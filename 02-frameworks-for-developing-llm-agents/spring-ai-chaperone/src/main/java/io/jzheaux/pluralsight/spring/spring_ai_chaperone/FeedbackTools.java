package io.jzheaux.pluralsight.spring.spring_ai_chaperone;

import java.util.List;

import org.springframework.ai.document.Document;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Component;

@Component
public class FeedbackTools {

  private final VectorStore vectors;

  public FeedbackTools(VectorStore vectors) {
    this.vectors = vectors;
  }

  @Tool(description = "Save Student Feedback")
  public void saveStudentFeedback(String feedback) {
    this.vectors.add(List.of(new Document(feedback)));
  }
}
