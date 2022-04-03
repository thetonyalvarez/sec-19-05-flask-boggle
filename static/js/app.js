$(() => {

	console.log("start js")

	const $form = $("#guess-form");
	const $input = $("#guess-input");
	const $submit = $("#guess-submit");
	const $foundWords = $("#found-words")
	const $messageWrapper = $("#message-wrapper")
	const $scoreWrapper = $("#score-wrapper")
	const $timerWrapper = $("#timer-wrapper")
	const $highScoreWrapper = $("#high-score-wrapper")
	const $gamesPlayedWrapper = $("#games-played-wrapper")
	const $newGameBtn = $("#new-game-btn-wrapper")

	console.log($form)
	console.log($input)

	const searchForWord = async (searchTerm) => {
		console.debug("searchForWord", searchTerm)
		const res = await axios({
			url: '/user-guess',
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json; charset=utf-8'
			},
			data: {
				guess: searchTerm,
				board
			},
		})

		return res.data

	}

	const addToWordList = (word) => {
		console.debug("addToWordList", word)

		$foundWords.append($("<li>").append(word))
	}

	const showMessage = (result, resp) => {
		console.debug("showMessage", result, resp)

		$messageWrapper.empty()

		if (result == "ok") {
			$messageWrapper.append(`<p>${resp} is ok.</p>`)
		}
		if (result == "not-word") {
			$messageWrapper.append(`<p>${resp} is not a word.</p>`)
		}
		if (result == "not-on-board") {
			$messageWrapper.append(`<p>${resp} is not on this board.</p>`)
		}

	}


	const showList = (list) => {
		console.debug("showList", list)

		$foundWords.empty()
		list.forEach((item) => addToWordList(item))
	}

	let finalScore = 0

	const calculateScore = (found_words) => {
		console.debug("calculateScore", found_words)

		let tempScore = 0

		found_words.forEach(word => {
			tempScore += word.length
		})

		finalScore = tempScore

		return finalScore
	}


	const submitWordGuess = async (e) => {
		console.debug("submitWordGuess", e)
		e.preventDefault();

		// assign input value to the search function
		const res = await searchForWord($input[0].value);

		const { resp: {found_words, last_searched_word}, result } = res

		// Show score
		let score = calculateScore(found_words)

		$scoreWrapper.empty()
		$scoreWrapper.append($(`<div>Current Score: ${score}</div>`))

		// Show message
		showMessage(result, last_searched_word)

		// Show List
		showList(found_words)

		// reset input value to empty
		$input[0].value = "";

	}

	const showHighScore = (score) => {
		console.debug("showHighScore", score)

		$highScoreWrapper.empty()
		$highScoreWrapper.append($(`<div>High Score: ${score}</div>`))
	}

	const showGamesPlayed = (games_played) => {
		console.debug("showGamesPlayed", games_played)

		$gamesPlayedWrapper.empty()
		$gamesPlayedWrapper.append($(`<div>Games Played: ${games_played}</div>`))
	}

	const gameCompleted = async () => {
		console.debug("gameCompleted")

		const res = await axios({
			url: '/game-over',
			method: 'post',
			data: {
				finalScore
			}
		})
		const {high_score, games_played} = res.data
		showHighScore(high_score)
		showGamesPlayed(games_played)

	}

	const showNewGameBtn = () => {
		console.debug('showNewGameBtn')
		
		$newGameBtn.empty()
		$form.empty()
		$newGameBtn.append($(`<form action="/restart">
		<button class="btn btn-primary" type="submit">New Game</button>
		</form>`))
	}

	// Timer function
	let sec = 10
	let timer = setInterval(() => { 
		$timerWrapper.text(`Timer: ${sec--}`);
		if (sec == -1) {
			$input.prop('disabled', true)
			$submit.prop('disabled', true)

			gameCompleted();
			showNewGameBtn();

			clearInterval(timer);
		} 
	}, 1000);

	$form.on("submit", submitWordGuess);

})