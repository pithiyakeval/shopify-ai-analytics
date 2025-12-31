require "net/http"
require "json"

class AiServiceClient
  AI_SERVICE_URL = "http://127.0.0.1:8000/ask"

  def self.ask_question(store_id, question)
    uri = URI(AI_SERVICE_URL)

    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri, {
      "Content-Type" => "application/json"
    })

    request.body = {
      store_id: store_id,
      question: question
    }.to_json

    response = http.request(request)
    JSON.parse(response.body)
  rescue StandardError => e
    {
      answer: "AI service unavailable",
      confidence: "low",
      error: e.message
    }
  end
end
