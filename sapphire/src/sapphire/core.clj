(ns sapphire.core)
(:require
 '[sapphire.assistant :as assistant])
(require
 '[sapphire.plugins.gpt :as gpt])

(defn perpetual-loop []
  (loop []
    (let [input (read-line)]
      (println (sapphire.plugins.gpt/chat-with-assistant input))
      (recur))))

(perpetual-loop)