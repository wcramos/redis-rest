# redis-rest
Redis REST API usage exercise

# Run instructions
Before running the program, set API_URL, API_USER, and API_PASSWORD as environment variables.

export API_URL="https://re-cluster1.ps-redislabs.org:9443"
export API_USER="your_username"
export API_PASSWORD="your_password"

After setup the API you can run:

Usage: python script.py <CDB | CUSR | LUSR | DDB <db_id>>

CDB = Create a New Database (my-redis-db)
CUSR = Create Three New Users with default password "my-password"
LUSR = List and Display Users
DDB <UID> = Delete the Created Database (need to enter the database UID)




