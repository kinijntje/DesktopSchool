package main

import (
	"context"
	"log"
	"math/rand"
	"net"
	"strconv"

	"google.golang.org/grpc"
	pb "hoard.com/grpc/pkg"
)

const (
	port = ":50051"
)

var hoards []*pb.HoardInfo

type hoardServer struct {
	pb.UnimplementedHoardServer
}

func main() {
	initHoards()
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()

	pb.RegisterHoardServer(s, &hoardServer{})

	log.Printf("server listening at: %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
}

func initHoards() {
	hoard1 := &pb.HoardInfo{Id: "1",
		Title: "The Batman", Sender: &pb.Sender{
			Firstname: "Matt", Lastname: "Reeves"}}
	hoard2 := &pb.HoardInfo{Id: "2",
		Title: "Doctor Strange in the Multiverse of Madness",
		Sender: &pb.Sender{Firstname: "Sam",
			Lastname: "Raimi"}}

	hoards = append(hoards, hoard1)
	hoards = append(hoards, hoard2)
}

func (s *hoardServer) GetHoards(in *pb.Empty, stream pb.Hoard_GetHoardsServer) error {
	log.Printf("Received: %v", in)
	for _, hoard := range hoards {
		if err := stream.Send(hoard); err != nil {
			return err
		}
	}
	return nil
}

func (s *hoardServer) GetHoard(ctx context.Context, in *pb.Id) (*pb.HoardInfo, error) {
	log.Printf("Received: %v", in)

	res := &pb.HoardInfo{}

	for _, hoard := range hoards {
		if hoard.GetId() == in.GetValue() {
			res = hoard
			break
		}
	}

	return res, nil
}

func (s *hoardServer) CreateHoard(ctx context.Context, in *pb.HoardInfo) (*pb.Id, error) {
	log.Printf("Received: %v", in)
	res := pb.Id{}
	res.Value = strconv.Itoa(rand.Intn(100000000))
	in.Id = res.GetValue()
	hoards = append(hoards, in)
	return &res, nil
}

func (s *hoardServer) UpdateHoard(ctx context.Context, in *pb.HoardInfo) (*pb.Status, error) {
	log.Printf("Received: %v", in)

	res := pb.Status{}
	for index, hoard := range hoards {
		if hoard.GetId() == in.GetId() {
			hoards = append(hoards[:index], hoards[index+1:]...)
			in.Id = hoard.GetId()
			hoards = append(hoards, in)
			res.Value = 1
			break
		}
	}

	return &res, nil
}

func (s *hoardServer) DeleteHoard(ctx context.Context, in *pb.Id) (*pb.Status, error) {
	log.Printf("Received: %v", in)

	res := pb.Status{}
	for index, hoard := range hoards {
		if hoard.GetId() == in.GetValue() {
			hoards = append(hoards[:index], hoards[index+1:]...)
			res.Value = 1
			break
		}
	}

	return &res, nil
}
