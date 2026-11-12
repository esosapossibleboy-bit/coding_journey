function getTopAppNames(apps, minRating) {
    return apps
        .filter(app => app.rating >= minRating)
        .map(app => app.name);
}

module.exports = { getTopAppNames };