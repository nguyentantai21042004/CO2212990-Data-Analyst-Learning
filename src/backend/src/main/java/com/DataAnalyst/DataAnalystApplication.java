package com.DataAnalyst;

import com.opencsv.CSVReader;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.FileReader;

@SpringBootApplication
public class DataAnalystApplication {

	public static void main(String[] args) {
		String csvFile = "path/to/your/file.csv"; // Đường dẫn đến file CSV
		String mongoUri = "mongodb://localhost:27017"; // Địa chỉ MongoDB
		String databaseName = "yourDatabase";
		String collectionName = "yourCollection";

		try (CSVReader reader = new CSVReader(new FileReader(csvFile))) {
			MongoClientURI uri = new MongoClientURI(mongoUri);
			MongoClient mongoClient = new MongoClient(uri);
			MongoDatabase database = mongoClient.getDatabase(databaseName);
			MongoCollection<Document> collection = database.getCollection(collectionName);

			String[] nextLine;
			while ((nextLine = reader.readNext()) != null) {
				// Giả sử file CSV có 5 cột: Date, Time, Comment, Credit, Name
				Document doc = new Document("date", nextLine[0])
						.append("time", nextLine[1])
						.append("comment", nextLine[2])
						.append("credit", nextLine[3])
						.append("name", nextLine[4]);

				collection.insertOne(doc); // Đẩy tài liệu vào MongoDB
			}

			mongoClient.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
