# Card Guessing Game

This is a simple Python card game where you guess whether your card is greater or less than the house's card. The game can be played via a Tkinter GUI or in the console.

---

## 🛠 How to Run

It is recommended to use **Miniconda** or **Anaconda** to create an isolated environment.

1. Clone the repository:

```bash
git clone https://github.com/your-username/card-guessing-game.git
cd card-guessing-game
````

2. Create and activate the environment using the provided `environment.yml`:

```bash
conda env create -f environment.yml
conda activate cardgame
```

3. Run the game:

   * For **GUI version**:

     ```bash
     python gui_app.py
     ```

   * For **console version**:

     ```bash
     python app.py
     ```

---

## 🎮 How to Play

* You start with a certain number of points.
* Each match costs points to play.
* A card is dealt to the house.
* You must guess whether your card will be **greater (g)** or **less (l)**.
* If you guess correctly:

  * You can choose to **stop** and take your reward.
  * Or **continue** to double the reward by guessing again.
* If you guess wrong, you lose the match and the points.
* The game ends if you:

  * Reach the **win threshold** → 🏆 You win!
  * Drop below the **lose threshold** → ❌ Game over.

---

## 📦 Project Structure

```
card-guessing-game/
├── gui_app.py         # GUI version using Tkinter
├── app.py             # Console version
├── src/
│   ├── game.py        # Game logic
│   ├── match.py       # Match logic and card dealing
│   └── card.py        # Card comparison logic
├── environment.yml    # Conda environment file
└── README.md          # Project instructions
```

---

## 🧠 Requirements

* Python 3.8+
* Tkinter (usually preinstalled)
* All other dependencies are handled by `environment.yml`

---

## 📋 License

This project is for demo purposes.

