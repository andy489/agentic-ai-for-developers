package io.jzheaux.pluralsight.spring.spring_ai_chaperone;

import java.net.URI;
import java.time.ZonedDateTime;
import java.util.List;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class WeatherTools {

  private final String weatherUrl;

  public WeatherTools(ChaperoneProperties props) {
    this.weatherUrl = props.weatherUrl();
  }

  @Tool(description = "Get Weather Forecast")
  public List<WeatherResponse> getWeatherForecast() {
    RestTemplate rest = new RestTemplate();
    Response response = rest.getForObject(URI.create(weatherUrl), Response.class);
    assert response != null;
    return response.properties().periods();
  }

  public record Response(Properties properties) {

  }

  public record Properties(List<WeatherResponse> periods) {

  }

  public record WeatherResponse(ZonedDateTime startTime, ZonedDateTime endTime, Integer temperature,
                                String windSpeed,
                                Precipitation probabilityOfPrecipitation, String shortForecast) {

  }

  public record Precipitation(Integer value) {

  }
}
