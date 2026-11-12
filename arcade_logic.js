function checkCollision(heroY, obstacleX) {
    return obstacleX > 250 && obstacleX < 320 && heroY > 220;
}

module.exports = { checkCollision };