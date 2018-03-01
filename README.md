# Minifilebox
A simple dropbox-like solution.

Minifilebox allows to handle upload, download, delete, list files.
When a fine is uploaded, it is splitted in chunks of configurable size which are store in distributed, replicated DB.

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

# Deployment

* Requirements
  * Docker: the applications in Dockers
  
* How To Run
  * Run the run_all.sh script

