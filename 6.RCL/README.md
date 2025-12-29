# ROS 2 Client Library (RCL) Guide

![ROS Client Library API Stack](images/ros_client_library_api_stack.png)

## What is a ROS 2 Client Library?

A ROS 2 client library provides:

- Node creation
- Publishers / Subscribers
- Services / Clients
- Actions
- Parameters
- Timers, callbacks, executors
- QoS configuration (Reliability, Durability, History, etc.)

It hides DDS complexity and gives a clean, language-friendly API.

## Main Client Libraries in ROS 2

### 1. rclcpp (C++)

- Most powerful and performant
- Fine-grained control over memory and execution
- Used in real-time and production robots

**Example:**

```cpp
#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("cpp_node");
  rclcpp::spin(node);
  rclcpp::shutdown();
}
```

### 2. rclpy (Python)

- Easy to learn and rapid development
- Slightly less performance than C++
- Widely used for prototyping and orchestration

**Example:**

```python
import rclpy
from rclpy.node import Node

rclpy.init()
node = Node("py_node")
rclpy.spin(node)
rclpy.shutdown()
```

### Other Client Libraries

| Library  | Language | Use Case                  |
|----------|----------|---------------------------|
| rcljava  | Java     | Android / JVM-based robotics |
| rclcs    | C#       | Unity, .NET               |
| rclrs    | Rust     | Safety-critical systems   |
| rclgo    | Go       | Cloud & tooling integrations |

## Services and Clients in ROS 2

Services follow a **Request–Response Model**.

- Think of it like a function call over the network.
- **Client** → sends a request
- **Server** → processes it
- **Server** → sends back a response
- **Client** → receives the response

Unlike topics (continuous data stream), services are one-time interactions.

## Structure of a Service

Each service is defined using a `.srv` file, which has two parts:

- **Request**
- **Response** (separated by `---`)

**Example: AddTwoInts.srv**

```
int64 a
int64 b
---
int64 sum
```

- **Request:** a, b
- **Response:** sum

## Client–Server Process Flow

1. Client node sends a request (e.g., a = 5, b = 10)
2. Service server node receives the request
3. Server processes the logic (e.g., sum = 5 + 10 = 15)
4. Server sends response
5. Client receives the response

This interaction happens only once per request.

## Service Server (Python – rclpy)

A service server:

- Waits for requests
- Executes a callback function
- Sends back a response

**Example: Service Server**

```python
self.srv = self.create_service(
    AddTwoInts,
    'add_two_ints',
    self.callback
)

def callback(self, request, response):
    response.sum = request.a + request.b
    return response
```

- `callback()` is triggered automatically
- Server must be spinning: `rclpy.spin(node)`

## Client Node (Python – rclpy)

A client:

- Sends a request
- Waits for response (sync or async)

**Create Client:**

```python
client = self.create_client(AddTwoInts, 'add_two_ints')
```

**Wait Until Service Is Available:**

```python
client.wait_for_service(timeout_sec=1.0)
```

**Send Request (Async):**

```python
future = client.call_async(request)
```

**Get Response:**

```python
rclpy.spin_until_future_complete(node, future)
response = future.result()
```

## Synchronous vs Asynchronous Clients

- **Synchronous Client:**
  - Blocks execution
  - Waits until response arrives
  - Simple but can freeze the node

- **Asynchronous Client (Recommended):**
  - Non-blocking
  - Node continues working
  - Response handled later

Most ROS 2 applications prefer async clients.

## Spin Mechanism (rclpy.spin())

Why is `spin()` required?

- ROS 2 communication is event-driven.
- Handles incoming requests
- Executes callbacks
- Processes service responses

Without `spin()`:
- No callbacks
- No service communication

## Industrial Use Cases

Services are used for commands, not continuous data.

Examples:

- Turn robot LED ON/OFF
- Reset sensor
- Start/stop motor
- Change robot mode
- Set speed or configuration

If the action needs confirmation, use a service.

## ROS Middleware (RMW) – Why It Exists

RMW (ROS Middleware Interface) is a bridge layer between:

- ROS client libraries (rclpy, rclcpp)
- DDS implementations (Fast DDS, Cyclone DDS, etc.)

```
ROS Node (rclpy)
     ↓
RCL
     ↓
RMW
     ↓
DDS
     ↓
Network
```

This abstraction allows DDS vendor independence.

## DDS (Data Distribution Service)

DDS is the actual communication engine used by ROS 2.

It handles:

- Discovery
- Serialization
- QoS
- Real-time communication

## DDS Implementations Comparison

| DDS          | Real-Time | License  | Notes                          |
|--------------|-----------|----------|--------------------------------|
| Fast DDS     | Yes       | Apache 2 | ROS 2 default                  |
| Cyclone DDS  | Yes       | Eclipse  | Lightweight & fast             |
| RTI Connext  | Yes       | Paid     | Industrial-grade               |

**Key Notes:**

- Fast DDS → Default, good balance
- Cyclone DDS → Better performance in some real-time cases
- RTI Connext → Used in aerospace, automotive (paid)

You can switch DDS without changing your ROS code.

## How Services Use DDS Internally

Even though services feel like request–response, DDS uses:

- Topics
- Hidden request/response topics
- QoS policies

ROS 2 hides this complexity using RMW.

## Summary

- **Service** = One-time request–response
- **Client** = Sends request
- **Server** = Processes and responds
- **Spin** = Needed for callbacks
- **Async client** = Best practice
- **RMW** = ROS ↔ DDS bridge
- **DDS** = Actual transport layer