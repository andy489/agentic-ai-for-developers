package io.jzheaux.pluralsight.spring.spring_ai_chaperone;

import java.util.List;

import org.jspecify.annotations.NonNull;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.core.io.Resource;

@SpringBootApplication
@EnableConfigurationProperties(ChaperoneProperties.class)
public class SpringAiChaperoneApplication implements CommandLineRunner {

	private final VectorStore vectors;
	private final List<Resource> resources;

	public SpringAiChaperoneApplication(VectorStore vectors,
			@Value("classpath:rag/*.txt") List<Resource> resources) {
		this.vectors = vectors;
		this.resources = resources;
	}

	static void main(String[] args) {
		SpringApplication.run(SpringAiChaperoneApplication.class, args);
	}

	@Override
	public void run(String @NonNull ... args) {
		this.resources.forEach((r) -> {
			List<Document> documents = new TextReader(r).read();
			documents = TokenTextSplitter.builder().build().transform(documents);
			this.vectors.add(documents);
		});
	}

}
