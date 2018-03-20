# Minifilebox
A simple dropbox-like solution.

Minifilebox allows to upload, download, delete, list files.
When a fine is uploaded, it is split in chunks of configurable size which are store in distributed, replicated storage.

Minifilebox exports REST endpoints to perform operations

* File Upload:

        curl -X POST http://<host:port>/minifilebox/api/v1/files/upload \
            -H 'cache-control: no-cache' \
            -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
            -F file=@<your_file>
         
         Output:
         {
            "chunk_size": <chunk_size>,
            "chunks": [
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24
            ],
            "file_id": <file_unique_id>,
            "file_name": <file_name>
        }
        
* File Download:

        curl -X GET http://<host:port>/minifilebox/api/v1/files/download/<file_id> \
            -H 'cache-control: no-cache'
            
* File Delete:

       curl -X DELETE http://<host:port>/minifilebox/api/v1/files/delete/<file_id> \
            -H 'cache-control: no-cache'
           
* Files List:

       curl -X GET http://<host:port>/minifilebox/api/v1/files
            -H 'cache-control: no-cache'

# Project Structure

* **file_storage**: it is provide the core functionalities for handling the files inside the system, splitting them and managing the associated metadata.
    
    * **[FileStorage](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/FileStorage.py)** class implements the core logic. It calls the ObjectStore interface to store files chunks and with the ContextInterface for storing file metadata (Minifile)
    * **[ObjectStoreInterface](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/StorageInterface.py)** class provides the methods to interact with the chunks storage
    * **[ContextStoreInterface](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/StorageInterface.py)** class provides the methods to interact with the Minifile storage
    * **[MemoryStorage](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/MemoryStorage.py)** module provides the implementation of the StorageInterface when using a simple memory DB. Aimed for testing
    * **[CassandraStorage](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/CassandraStorage.py)** module provides the implementation of the StorageInterface when the system is backed by Cassandra DB
    * **[HTTPProxyStorage](https://github.com/sbisogni/minifilebox/blob/master/file_storage/file_storage/HTTPProxyStorage.py)** module provides the implementation of the StorageInterface when the storage systems are remote services which can be contected by HTTP Rest endpoints (*Not Finalized*)
    
  This structure allows to instantiate of the FileStorage class with different configurations allowing the system to easily scale and distributing each component of the system if required
  
* **components**: here is where are located the different applications which will run inside dedicated Docker containers

    * **[file_service](https://github.com/sbisogni/minifilebox/blob/master/components/file_service)** application provides the rest endpoints to interact with the Minifilebox system. Check the [config.py](https://github.com/sbisogni/minifilebox/blob/master/components/file_service/config.py) to see configuration options. 
    * **[contextstore_service](https://github.com/sbisogni/minifilebox/tree/master/components/contextstore_service)** the file metadata storage. Check the [config.py](https://github.com/sbisogni/minifilebox/blob/master/components/objectstore_service/config.py) to see configuration options.
    * **[objectstore_service](https://github.com/sbisogni/minifilebox/tree/master/components/objectstore_service)** the chunk storage. Check the [config.py](https://github.com/sbisogni/minifilebox/blob/master/components/contextstore_service/config.py) to see configuration options. 
    
# Deployment

* Requirements
  * [docker](https://www.docker.com/)
  * [docker-compose](https://docs.docker.com/compose/)
  
  This is the only requirement if you want to run the application. Docker will take care to all the rest.
  To run the unittest and integration test the following are also required:
  
  * [python 3](https://www.python.org/download/releases/3.0/)
  * [pip3](https://pypi.python.org/pypi/pip)
  * [virtualenv](https://virtualenv.pypa.io/en/stable/) (optional, if you do not want to mess with your python env)
  
* How To Run Minifilebox

        git clone https://github.com/sbisogni/minifilebox.git
        cd minifilebox
        ./bin/run_all.sh

The file service is now running on 0.0.0.0. This is the entry point for the rest endpoints. You can target it to the URI: 

    http://0.0.0.0:5000/minifileboc/api/v1/files


* How to Run Unittest and Integration Tests

Prepare the python environment 

        cd minifilebox
        virtualenv 
        source env/bin/activate
        pip install -r requirements.txt
        
Now that the environment is ready you can run both unittest and integration tests
Unittest are implemented for the core file_storage package.

For unittest run 
   
        ./bin/run_unittest.sh 

For integration tests run

        ./bin/run_integration_tests.sh

