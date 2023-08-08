(ns sapphire.gpt)
(require '[wkok.openai-clojure.api :as api])

(def empty-chat [{:role "system" :content "You are a helpful assistant named Sapphire.EXE. your purpose is to help me manage my schedule, projects, and ADHD"}
                            {:role "assistant" :content "What is your name and purpose?"}])

                 
(println (get-in (api/create-chat-completion {:model "gpt-3.5-turbo"
                                              :messages empty-chat})[:choices 0 :message :content]))

(println (get-in (api/create-chat-completion {:model "gpt-3.5-turbo"
                                                :messages [{:role "system" :content "You are a helpful assistant."}
                                                           {:role "user" :content "Who won the world series in 2020?"}
                                                           {:role "assistant" :content "The Los Angeles Dodgers won the World Series in 2020."}
                                                           {:role "user" :content "Where was it played?"}]})[:choices 0 :message :content] ))

