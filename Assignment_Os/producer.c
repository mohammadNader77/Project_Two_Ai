#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/wait.h>

#define Buffer_Size 10

struct BUFFER {
    int data[Buffer_Size]; //declaration array with size (Buffer_Zize)
    int r_index; //declaration r_index for read from buffer
    int w_index; // declaration w_index for write into buffer
};

//function for add item to the buffer
void produce_item(struct BUFFER* buffer) { 

    int item = rand() % 100; //select item in random 
    buffer->data[buffer->w_index] = item;  //add item to array
    //function for add item to the buffer
    buffer->w_index = (buffer->w_index + 1) % Buffer_Size; 
    printf("Add Item To Buffer(Produced): %d\n", item);
}

//function to add all item to buffer before the consumer read item from buffer
void producer(struct BUFFER* buffer) { 
  //declaration variable with the buffer size 
  int number_of_items = Buffer_Size; 
     while (number_of_items > 0) { 

        // Check if the buffer still has empty 
        if (((buffer->w_index + 1) % Buffer_Size) != buffer->r_index) {
            produce_item(buffer);
            //number_of_items--; //for infinite loop 
        }
        
        else
      {
        // Wait for the consumer to read the all item from the buffer
        while (((buffer->r_index + 1) % Buffer_Size) == buffer->w_index) {
            usleep(1000);
        }
    }
    }
}


int main() {
    const char* shm_name = "/shm_buffer";
    //open the shared memory object
    int shm_fd = shm_open(shm_name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        printf("error : shm_open failed");
        return 1;
    }
    if (ftruncate(shm_fd, sizeof(struct BUFFER)) == -1) {
        printf("error : ftruncate failed");
        return 1;
    }
    struct BUFFER* buffer = mmap(NULL, sizeof(struct BUFFER),
                              PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (buffer == MAP_FAILED) {
        printf("error : mmap failed");
        return 1;
    }
    
    buffer->r_index = 0; //restart the buffer_index 
    buffer->w_index = 0; //restart the buffer_index 
    
    pid_t pid = fork(); //fork a child process
    
    if (pid == -1) {
        printf("error : fork failed");
        return 1;
    }
    else if (pid == 0) { //child process 
          execl("./consumer","./consumer", NULL); //name of the consumer
          printf("error : execl failed");
          return 1;
    } 
    else { //partner will wait for the child to complete 
        producer(buffer);
        wait(NULL);
        if (munmap(buffer, sizeof(struct BUFFER)) == -1) {
        printf("error : munmap failed");
        return 1;
        
        }
        if (shm_unlink(shm_name) == -1) {
            printf("error : shm_unlink failed");
            return 1;
        }
    }
    return 0;
}