package main

import (
	"database/sql"
	"fmt"
	"log"
	"net"
	"strings"

	_ "github.com/lib/pq"
)

func handleRequest(conn net.Conn, db *sql.DB) {
	defer conn.Close()
	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		log.Println(err)
		return
	}

	request := strings.TrimSpace(string(buffer[:n]))

	if strings.Contains(request, "`") {
		// Запрос 2
		var openkey string
		err := db.QueryRow("SELECT openkey FROM usr_info WHERE usr = $1", request).Scan(&openkey)
		if err == sql.ErrNoRows {
			conn.Write([]byte("bad_user"))
			return
		}
		conn.Write([]byte(openkey))

	} else if strings.Contains(request, "+") {
		fmt.Println("Тип запроса - пересылка сообщения")
		parts := strings.Split(request, "+")
		login := parts[0]
		message := parts[1]

		// Запрос 3
		var recipient string
		err := db.QueryRow("SELECT usr FROM usr_info WHERE usr = $1", login).Scan(&recipient)
		if err != nil {
			conn.Write([]byte("Recipient does not exist"))
			return
		}
		conn.Write([]byte(fmt.Sprintf("Sending message '%s' to %s", message, recipient)))

	} else if strings.Contains(request, "~") {
		parts := strings.Split(request, "~")
		login := parts[0]
		password := parts[1]

		fmt.Println("Тип запроса - логин/регистрация")
		fmt.Println("login - ", login)
		fmt.Println("password - ", password)
		fmt.Println("")

		// Запрос 1
		var storedPassword string
		err := db.QueryRow("SELECT paswd FROM autor WHERE usr = ", login).Scan(&storedPassword)
		fmt.Println("storedPassword - ", storedPassword)
		if err == sql.ErrNoRows {
			_, err = db.Exec("INSERT INTO autor (usr, paswd) VALUES ($1, $2)", login, password)
			if err != nil {
				log.Println(err)
				conn.Write([]byte("Error creating user"))
				return
			} else {
			}
			conn.Write([]byte("User created successfully"))
			return
		} else if storedPassword == password {
			conn.Write([]byte("Login successful"))
		} else {
			conn.Write([]byte("Bad password"))
		}
	}
}

func main() {
	db, err := sql.Open("postgres", "host=localhost port=5432 user=postgre password=12345 dbname=PostgreSQLRGZ sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	listener, err := net.Listen("tcp", ":6575")
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err.Error())
		return
	}

	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Ошибка при принятии соединения:", err.Error())
			continue
		}
		fmt.Println("Сервер запущен...")
		go handleRequest(conn, db)
	}
}
