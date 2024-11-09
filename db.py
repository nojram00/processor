import pymongo
from datetime import datetime

MONGODB_URI = "mongodb+srv://marjongodito0505:nojramnojram12345@app.t1uvd.mongodb.net/?retryWrites=true&w=majority&appName=App"

client = pymongo.MongoClient(MONGODB_URI)

database = client["App"]

processor_log = database["processor_log"]

def save_log(message):
    log = processor_log.insert_one({
        "timestamp" : datetime.now(),
        "log" : message
    })

    print(f"Log added: {log}")

if __name__ == '__main__':
    save_log("Added test")
