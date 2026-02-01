FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-w -s" -o momento cmd/momento/main.go

FROM alpine:3.20

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

RUN addgroup -g 1000 momento && \
    adduser -D -u 1000 -G momento momento

COPY --from=builder /app/momento /usr/local/bin/
COPY --from=builder /app/configs/config.yaml.example /configs/config.yaml

RUN chown -R momento:momento /configs

USER momento

EXPOSE 8080

CMD ["/usr/local/bin/momento"]
