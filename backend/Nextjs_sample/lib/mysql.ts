
import { createConnection } from 'mysql2'
import info from './model';

let dbConnection;
try {
    dbConnection = createConnection({
        host: 'localhost',
        user: 'root',
        password: '1234',
        database: 'test'
    });
} catch (err) {
    console.error(err);
}

let clientPromise
clientPromise = dbConnection


function queryPromise(queryString) :Promise<Array<info>> {  
	return new Promise((resolve, reject) => {  
		clientPromise.query(queryString, (error, results) => {  
			if (error) {  
				return reject(error);  
			}  
			resolve(results);  
		});  
	});  
}  


export {clientPromise, queryPromise}