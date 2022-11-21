const driverSelect = $("#driverSelect");
const statsSpinner = $("#statsSpinner");
const statsDiv = $("#statsDiv");
const chartsSpinner = $("#chartsSpinner");
const chartsDiv = $("#chartsDiv");

driverSelect.on("change", function () {
    const driverId = $(this).val();
    fetchStats(driverId);
    fetchCharts(driverId);
});

//Load all the drivers from the API
const url = "http://127.0.0.1:8000/drivers";
fetch(url)
    .then((response) => response.json())
    .then((data) => {
        data.forEach(function (item) {
            const driverId = item.driver.value
                .split("#")[1]
                .replace("driver", "");
            const name = item.name.value;
            driverSelect.append(`<option value="${driverId}">${name}</option>`);
        });
        driverSelect.selectpicker("refresh");
    });

/**
 * Given the ID of a driver retrieves from the backend API the data and modifies the DOM
 * showing the stats for the given driver
 * @param {*} driverId
 */
function fetchStats(driverId) {

    statsSpinner.show();
    statsDiv.hide();

    const d_champ = $("#driverChampionships");
    const seasons = $("#seasons");
    const races = $("#races");
    const pol = $("#pol");
    const victories = $("#victories");
    const percVictories = $("#percVictories");
    const podiums = $("#podiums");
    const percPodiums = $("#percPodiums");
    const bestQuali = $("#bestQuali");
    const worstQuali = $("#worstQuali");
    const bestRace = $("#bestRace");
    const worstRace = $("#worstRace");
    const q3times = $("#q3times");
    const dnf = $("#dnf");
    const cleanRaces = $("#cleanRaces");
    const cons = $("#cons");
    const consWin = $("#consWin");
    const cards = [
        d_champ,
        cons,
        consWin,
        seasons,
        races,
        pol,
        victories,
        percVictories,
        podiums,
        percPodiums,
        bestQuali,
        worstQuali,
        bestRace,
        worstRace,
        q3times,
        dnf,
        cleanRaces,
    ];
    fetch(url + "/" + driverId + "/stats")
        .then((response) => response.json())
        .then((data) => {
            let i = 0;
            const param = [
                "cp_win",
                "constructor",
                "constructor_win",
                "season_number",
                "races_number",
                "pole_number",
                "victories_number",
                "perc_vic_races",
                "podiums",
                "perc_pod_races",
                "best_quali",
                "worst_quali",
                "best_race",
                "worst_race",
                "q3_quali",
                "dnf",
                "victory_from_pole",
            ];
            data["perc_vic_races"] =
                parseFloat(data["perc_vic_races"]).toFixed(2) + "%";
            data["perc_pod_races"] =
                parseFloat(data["perc_pod_races"]).toFixed(2) + "%";
            param.forEach(function (el) {
                cards[i++].text(data[el]);
            });

            statsSpinner.hide();
            statsDiv.show();
        });
}

/**
 * Given the ID of a driver retrieves from the backend API the data and modifies the DOM
 * showing the resulting charts
 * @param {*} driverId
 */
function fetchCharts(driverId) {

    chartsSpinner.show();
    chartsDiv.hide();

    fetch(url + "/" + driverId + "/charts")
        .then((response) => response.json())
        .then((data) => {

            var xValues = Object.keys(
                data["driver_championship_points_year_by_year"]
            );
            var yValues = Object.values(
                data["driver_championship_points_year_by_year"]
            );
            var barColors = ["black "];
            new Chart("pointCpYear", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [
                        {
                            backgroundColor: barColors,
                            data: yValues,
                        },
                    ],
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Points year per year in the Driver Championship",
                    },
                },
            });

            var xValues = Object.keys(
                data["driver_championship_positions_year_by_year"]
            );
            var yValues = Object.values(
                data["driver_championship_positions_year_by_year"]
            );
            var barColors = ["black "];
            new Chart("positionCpYear", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [
                        {
                            backgroundColor: barColors,
                            data: yValues,
                        },
                    ],
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Position year per year in the Driver Championship",
                    },
                },
            });

            var xValues = Object.keys(data["get_top_ten_position_by_year"]);
            var yValues = Object.values(data["get_top_ten_position_by_year"]);
            var barColors = ["black "];
            new Chart("top10year", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [
                        {
                            backgroundColor: barColors,
                            data: yValues,
                        },
                    ],
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Top 10 race finishes year per year",
                    },
                },
            });

            var xValues = Object.keys(data["get_top_five_position_by_year"]);
            var yValues = Object.values(data["get_top_five_position_by_year"]);
            var barColors = ["black "];
            new Chart("top5year", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [
                        {
                            backgroundColor: barColors,
                            data: yValues,
                        },
                    ],
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Top 5 race finishes year per year",
                    },
                },
            });

            chartsSpinner.hide();
            chartsDiv.show();
        });
}
