package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
	pb "ucdp.com/grpc/config"
)

type greetingServiceServer struct {
	pb.UnimplementedGreetingServiceServer
}

func (s *greetingServiceServer) SayHello(ctx context.Context, in *pb.Person) (*pb.Person, error) {
	log.Printf(in.Name)
	return &pb.Person{Name: "Hello, " + in.Name}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreetingServiceServer(s, &greetingServiceServer{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
