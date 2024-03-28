package main

import (
	"log"
	"net"

	server "github.com/golang/protobuf/protoc-gen-go/pkg"
	"google.golang.org/grpc"
)

func main() {

	lis, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := server.Server{}

	grpcServer := grpc.NewServer()

	server.RegisterChatServiceServer(grpcServer, &s)
	//&s == server struckt

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %s", err)
	}
}
