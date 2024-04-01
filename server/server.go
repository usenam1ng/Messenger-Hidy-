package main

import (
	"database/sql"
	"fmt"
	"log"
	"net"
	"strings"

	_ "github.com/lib/pq"
)

func registration_login(request string, db *sql.DB) string {
	parts := strings.Split(request, "~")
	login := parts[0]
	password := parts[1]
	openkey := parts[2]

	fmt.Println("Тип запроса - логин/регистрация")
	fmt.Println("login - ", login)
	fmt.Println("password - ", password)
	fmt.Println("")

	// Запрос 1
	var storedPassword string
	err := db.QueryRow("SELECT paswd FROM autor WHERE usr = '" + login + "'").Scan(&storedPassword)
	fmt.Println("storedPassword - ", storedPassword, " - ", len(storedPassword))
	if err == sql.ErrNoRows || storedPassword == "" {
		_, err = db.Exec("INSERT INTO autor (usr, paswd) VALUES ($1, $2)", login, password)
		if err != nil {
			log.Println(err)
		}
		_, err1 := db.Exec("INSERT INTO usr_info (usr, openkey) VALUES ($1, $2)", login, openkey)
		if err1 != nil {
			log.Println(err)
		}
		return "User created successfully"
	} else if storedPassword == password {
		_, err1 := db.Exec("UPDATE your_table SET column2 = $2, WHERE condition_column = $1", login, openkey)
		if err1 != nil {
			log.Println(err)
		}
		return "Login successful"
	} else {
		return "Bad password"
	}
}

func to_chat(request string, db *sql.DB) string {
	fmt.Println("Тип запроса - пересылка сообщения")
	parts := strings.Split(request, "+")
	login := parts[0]
	from := parts[1]
	message := parts[2]

	var count int
	err := db.QueryRow("SELECT count(*) FROM chat").Scan(&count)
	if err != nil {
		log.Fatal(err)
	}
	id := count + 1

	_, err1 := db.Exec("INSERT INTO chat (logn, frm, mess, idd) VALUES ($1, $2, $3, $4)", login, from, message, id)
	if err1 != nil {
		log.Println(err)
		return "fail sending message"
	}
	return "message send"
}

func handleRequest(conn net.Conn, db *sql.DB) {
	defer conn.Close()
	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		log.Println(err)
		return
	}

	request := strings.TrimSpace(string(buffer[:n]))
	if strings.Contains(request, "~ping~") {
		parts := strings.Split(request, " + ")
		fmt.Println(request, "------------")
		login := parts[1]

		fmt.Println(login, "------------")

		var frm string
		var mess string
		var id int

		err := db.QueryRow("SELECT logn, mess, idd FROM chat WHERE frm = $1 LIMIT 1", login).Scan(&frm, &mess, &id)
		if err != nil {
			log.Println(err)
		}
		_, err = db.Exec("DELETE FROM chat WHERE idd = $1", id)
		if err != nil {
			log.Println(err)
		}

		resp := frm + "+" + mess
		conn.Write([]byte(resp))
	} else if strings.Contains(request, "`") {
		// Запрос 2
		parts := strings.Split(request, "`")
		login := parts[0]
		var openkey string
		fmt.Println(login)
		err := db.QueryRow("SELECT openkey FROM usr_info WHERE usr = $1", login).Scan(&openkey)
		if err == sql.ErrNoRows {
			conn.Write([]byte("bad_user"))
			return
		}
		conn.Write([]byte(openkey))

	} else if strings.Contains(request, "+") {
		resp := to_chat(request, db)
		conn.Write([]byte(resp))
	} else if strings.Contains(request, "~") {
		resp := registration_login(request, db)
		conn.Write([]byte(resp))
	}

}

func main() {
	db, err := sql.Open("postgres", "host=localhost port=5432 user=postgres password=12345 dbname=postgres sslmode=disable")
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
		fmt.Println("______________________")
		go handleRequest(conn, db)
	}
}
