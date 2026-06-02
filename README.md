# Distributed Notification System

## Problem Statement

Modern applications often need to deliver large volumes of notifications reliably while maintaining low latency and resilience to failures. Traditional synchronous notification workflows can become bottlenecks, introduce tight coupling between services, and struggle to recover from transient failures.

## Solution

This project implements a distributed event-driven notification system that leverages Apache Kafka for message streaming, Redis for caching and rate limiting, PostgreSQL for persistence, and FastAPI for service orchestration.

The architecture is designed to support asynchronous message processing, fault tolerance, retry mechanisms, Dead Letter Queue (DLQ) handling, observability, and scalable deployment through containerized infrastructure.


## Architecture Diagram

Producer Service
        │
        ▼
   Kafka Topic
        │
        ▼
 Notification Consumer
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
Email  SMS     Push
Worker Worker Worker
        │
        ▼
 PostgreSQL
        │
        ▼
Prometheus
        │
        ▼
 Grafana

## Engineering Concepts Demonstrated

* Event-Driven Architecture
* Asynchronous Processing
* Message Queues and Streaming
* Distributed Systems Design
* Dead Letter Queue (DLQ) Handling
* Retry and Recovery Mechanisms
* Rate Limiting
* Fault Tolerance
* Observability and Monitoring
* Containerized Deployments
* Service Decoupling
