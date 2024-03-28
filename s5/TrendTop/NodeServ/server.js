// import { loadPackageDefinition, Server, ServerCredentials } from './node_modules/@grpc';
// import { loadSync } from '@grpc/proto-loader';

const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const PROTO_PATH = "./hoard.proto";
const SERVER_URI = "0.0.0.0:50051";

const hoards = []

const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);

const GetHoards = (call, callback) => {
    hoards.push({
        call,
    });
};

const server = new grpc.Server();

console.log(protoDescriptor)

server.addService(protoDescriptor.hoard.HoardService.service, {
    GetHoards
});

//server.bindAsync(SERVER_URI, grpc.ServerCredentials.createInsecure(), function(callback) {});
//server.bind(SERVER_URI, grpc.ServerCredentials.createInsecure())
server.bindAsync(
    SERVER_URI,
    grpc.ServerCredentials.createInsecure(),
    (err, port) => {
      if (err) {
        console.log(err)
      }
      server.start(port);
      console.log(`listening on port ${port}`)
    }
)


console.log("Server is running!");
