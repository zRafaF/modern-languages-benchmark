run:
	@go run cmd/go-benchmark.go $(IMAGE_INPUT_PATH) $(VECTOR_INPUT)

ifeq ($(OS),Windows_NT)
build:
	@echo Building for Windows
	@go build -o go-benchmark.exe cmd/go-benchmark.go
else
build:
	@echo Building for Linux
	@go build -o go-benchmark cmd/go-benchmark.go
endif

