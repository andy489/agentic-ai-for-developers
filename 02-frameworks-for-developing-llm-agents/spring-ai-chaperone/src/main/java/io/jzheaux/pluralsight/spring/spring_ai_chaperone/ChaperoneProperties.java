package io.jzheaux.pluralsight.spring.spring_ai_chaperone;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "chaperone")
public record ChaperoneProperties(String weatherUrl) {

}
