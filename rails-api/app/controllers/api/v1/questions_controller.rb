module Api
    module V1
      class QuestionsController < ApplicationController
        def create
          store_id = params[:store_id]
          question = params[:question]
  
          if store_id.blank? || question.blank?
            render json: { error: "store_id and question are required" }, status: :bad_request
            return
          end
  
          ai_response = AiServiceClient.ask_question(store_id, question)
          render json: ai_response, status: :ok
        end
      end
    end
  end
  