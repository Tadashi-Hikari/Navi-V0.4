(ns sapphire.core)
(:use
 '[sapphre.assistant :as assistant]
 '[sapphire.gpt :as gpt])

(defrecord Assistant [running-log tailored-prompt])

(def assistant (->Assistant (atom 'gpt/empty-chat) (atom 'gpt/empty-chat)))

(defn perpetual-loop []
  (loop []
    (let [input (read-line)]
      (println ('gpt/chat-with-assistant input))
      (recur))))

(perpetual-loop)