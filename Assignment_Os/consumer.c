#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/wait.h>

#define Buffer_Size 10

struct BUFFER {
    int data[Buffer_Size]; //declaration array with size (Buffer_Size)
    int r_index; //declaration r_index for read from buffer
    int w_index; // declaration w_index for write into buffer
};

//function for remove item from the buffer
int consume_item(struct BUFFER* buffer) {  
//translate the item from buffer to variable item
    int item = buffer->data[buffer->r_index]; 
    buffer->r_index = (buffer->r_index + 1) % Buffer_Size;
    printf("Consumed Item (Removed From Buffer): %d\n", item);
    return item;
}

void consumer(struct BUFFER* buffer) {
    while (1) {
        // Check if the buffer still has items to consume
        if (buffer->r_index != buffer->w_index) {
            consume_item(buffer);
        }
        // Wait for the producer to write all item to buffer
        while (buffer->r_index == buffer->w_index) {
            usleep(1000);
        }
    }
}

int main() {
    const char* shm_name = "/shm_buffer";
    int shm_fd = shm_open(shm_name, O_RDWR, 0666);
    
    if (shm_fd == -1) {
      printf("error : shm_open failed");
      return 1;
    }
    struct BUFFER* buffer = mmap(NULL, sizeof(struct BUFFER),
                              PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (buffer == MAP_FAILED) {
        printf("error : mmap failed");
        return 1;
    }
    
    printf("----------------------------------\n");
    consumer(buffer);
    if (munmap(buffer, sizeof(struct BUFFER)) == -1) {
        printf("error : munmap failed");
        return 1;
    }
    return 0;
}