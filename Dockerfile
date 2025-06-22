FROM golang:1.21 AS builder

WORKDIR /app
COPY go.mod ./
COPY . .
RUN go mod tidy
RUN CGO_ENABLED=1 go build -o main .

FROM golang:1.21
RUN apt-get update && apt-get install -y ca-certificates sqlite3 && rm -rf /var/lib/apt/lists/*
WORKDIR /root/

COPY --from=builder /app/main .

EXPOSE 8080
CMD ["./main"]