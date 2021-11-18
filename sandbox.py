def main():
    run = True

    def stop_run():
        global run
        run = False

    i = 0

    while run:
        i += 1

        if i == 10:
            stop_run()

        if i == 100:
            return

    print("Done")


if __name__ == "__main__":
    main()
