(ns sapphire.util)
(require
 '[clojure.java.shell :as shell]
 '[clojure.java.io :as io]
 '[clojure.data.json :as json])

(defn run-subprocess 
  "This runs a simple subprocess"
  [command]
  (let [process (:out (shell/sh command))]
    (println "Subprocess output:")
    (println (:out process))))

(run-subprocess "echo \"hello\"")

(defn setup-user-environment [])

(defn file-exists? [path]
  (.exists (io/file path)))

(defn check-for-config [file]
  (if (file-exists? file)
    (println "File exists")
    (println "File doesn't exist")))

(check-for-config "src/sapphire/core.clj")