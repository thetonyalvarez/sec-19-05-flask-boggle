console.log("start main")

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
const $gameDetailsWrapper = $("#game-details-wrapper")

const components = [
	$highScoreWrapper,
	$gamesPlayedWrapper,
	$newGameBtn,
	$scoreWrapper
];

function hidePageComponents() {
	
	components.forEach(c => {
		console.log(c)
		c.hide()
	})
}

function showPageComponents() {
	
	components.forEach(c => {
		console.log(c)
		c.show()
	})
}

function emptyWordListStart() {
	$foundWords.append($(`<span>No words found yet.</span>`))
}
			
hidePageComponents()
emptyWordListStart()