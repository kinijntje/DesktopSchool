package chat

import (
	"log"

	"golang.org/x/net/context"
)

type Server struct {
}

// func "s" is pointer to server, function-name(input) (output *Message refers to autogenerated code)
func (s *Server) SayHello(ctx context.Context, in *Message) (*Message, error) {
	log.Printf("Receive message body from client: %s", in.Body)
	return &Message{Body: "Hello From the Server!"}, nil
}

func (s *Server) GetUsers(ctx context.Context, in *User) (*Message, error) {
	log.Printf("Receive message from client test")
	return &Message{Body: "This is working well"}, nil
}