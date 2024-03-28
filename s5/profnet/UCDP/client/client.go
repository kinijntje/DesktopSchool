package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	pb "ucdp.com/grpc/config"
)

func main() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	client := pb.NewGreetingServiceClient(conn)

	runSayHello(client)
}

func runSayHello(client pb.GreetingServiceClient) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	req := &pb.Person{Name: "Pedro", Age: 32}
	res, err := client.SayHello(ctx, req)
	if err != nil {
		log.Fatalf("%v.Sayhello(_) = _, %v", client, err)
	}
	log.Printf("Person: %v", res)
}
