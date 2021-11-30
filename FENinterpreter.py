def feninterpreter(FENstring):
    ranks = FENstring.split("/")

    currentsquare = 1
    board = []

    for rank in ranks:
        for x in rank:

            if x.isnumeric():
                for i in range(currentsquare, currentsquare + int(x)):
                    board.append("none")

                currentsquare += int(x)

            else:
                board.append(x)
                currentsquare += 1


    return(board)