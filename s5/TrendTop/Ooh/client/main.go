package main

import (
	"context"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	pb "hoard.com/grpc/pkg"
)

const (
	address = "localhost:50051"
)

func main() {
	conn, err := grpc.Dial(address, grpc.WithInsecure(),
		grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	client := pb.NewHoardClient(conn)

	runGetHoards(client)
	runGetHoard(client, "1")
	runCreateHoard(client, "Spiderman Spiderverse", "Stan", "Lee")
	runUpdateHoard(client, "1", "Spiderman Spiderverse", "Peter", "Parker")
	runDeleteHoard(client, "1")
}

func runGetHoards(client pb.HoardClient) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.Empty{}
	stream, err := client.GetHoards(ctx, req)
	if err != nil {
		log.Fatalf("%v.GetHoards(_) = _, %v", client, err)
	}
	for {
		row, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("%v.GetHoards(_) = _, %v", client, err)
		}
		log.Printf("HoardInfo: %v", row)
	}
}

func runGetHoard(client pb.HoardClient, hoardid string) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.Id{Value: hoardid}
	res, err := client.GetHoard(ctx, req)
	if err != nil {
		log.Fatalf("%v.GetHoard(_) = _, %v", client, err)
	}
	log.Printf("HoardInfo: %v", res)
}

func runCreateHoard(client pb.HoardClient, title string, firstname string, lastname string) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.HoardInfo{Title: title,
		Sender: &pb.Sender{Firstname: firstname,
			Lastname: lastname}}
	res, err := client.CreateHoard(ctx, req)
	if err != nil {
		log.Fatalf("%v.CreateHoard(_) = _, %v", client, err)
	}
	if res.GetValue() != "" {
		log.Printf("CreateHoard Id: %v", res)
	} else {
		log.Printf("CreateHoard Failed")
	}

}

func runUpdateHoard(client pb.HoardClient, hoardid string, title string, firstname string, lastname string) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.HoardInfo{Id: hoardid,
		Title: title, Sender: &pb.Sender{
			Firstname: firstname, Lastname: lastname}}
	res, err := client.UpdateHoard(ctx, req)
	if err != nil {
		log.Fatalf("%v.UpdateHoard(_) = _, %v", client, err)
	}
	if int(res.GetValue()) == 1 {
		log.Printf("UpdateHoard Success")
	} else {
		log.Printf("UpdateHoard Failed")
	}
}

func runDeleteHoard(client pb.HoardClient, hoardid string) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.Id{Value: hoardid}
	res, err := client.DeleteHoard(ctx, req)
	if err != nil {
		log.Fatalf("%v.DeleteHoard(_) = _, %v", client, err)
	}
	if int(res.GetValue()) == 1 {
		log.Printf("DeleteHoard Success")
	} else {
		log.Printf("DeleteHoard Failed")
	}
}
