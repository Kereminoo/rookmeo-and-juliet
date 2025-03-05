# rookmeo-and-juliet
Rookmeo and juliet materialized into a python app.

## Explanation
Two rooks from each side are randomly chosen at the start of the game. These rooks must see each other to escape from the board. However, the two rooks are unknown to the player. If they accidentally take one of the rooks, the other one will switch sides and become a queen.

## Differences
To win the game, rookmeo and juliet must look at each other, which is different from the actual one, where they escaped from the back rank.
Also, when rookmeo or juliet are taken, the other rook still turns into a queen, but it doesn't go to the other side.

## How to use
> [!WARNING]
> Windows does not support case sensitivity by default. Because of that, the black pieces are missing in this repository. Remember to download the required images from somewhere like [greenchess](https://greenchess.net/info.php?item=downloads).

Clone the repository:
`git clone https://github.com/Kereminoo/rookmeo-and-juliet.git`

Install dependencies:
`pip install -r requirements.txt`

Run the program
`python main.py`

## Credits
The [original video](https://www.youtube.com/shorts/k6aI4LyrxV0) for the idea.
My friend for sending me the video.
