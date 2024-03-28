package main

import (
	"log"

	"golang.org/x/net/context"
	"google.golang.org/grpc"

	server "github.com/golang/protobuf/protoc-gen-go/pkg"
)

func main() {

	var conn *grpc.ClientConn
	conn, err := grpc.Dial(":9000", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %s", err)
	}
	defer conn.Close()

	c := server.NewChatServiceClient(conn)

	//message := chat.Message{Body: "Hello From Client!"}
	user := server.User{Name: "Alibab", Age: 69}

	response, err := c.GetUsers(context.Background(), &user)
	if err != nil {
		log.Fatalf("Error when calling SayHello: %s", err)
	}
	log.Printf("Response from server: %s", response.Body)

}
