'use strict'

export const average = arr => arr.reduce(( p, c ) => p + c, 0) / arr.length;
export const randomColor = (transparency) => `rgba(${Math.floor(Math.random() * (255 + 1))}, ${Math.floor(Math.random() * (255 + 1))}, ${Math.floor(Math.random() * (255 + 1))}, ${transparency})`

export function drawChart(chartLabels, chartDataset, chartType, title, ctx, myChart, scales={y: {min: 1, max: 5}}) {
    // Set Chart
    const data = {
        labels: chartLabels,
        datasets: Object.values(chartDataset).map((dataset) => {
            if(!('backgroundColor' in dataset)) {
                const color = randomColor(0.7)
                dataset.backgroundColor = color
                dataset.borderColor = color
            }
            dataset.tension = 0.2

            return dataset
        })
    }
    
    const config = {
        type: chartType,
        data: data,
        options: {
            scales: scales,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 20
                    }
                }
            }
        }
    }
    
    // draw Chart
    myChart.destroy()
    myChart = new Chart(ctx, config)

    return myChart
}

export function sortReviewsByDate(reviews) {
    let sortedReviews = {}

    for (const review of reviews) {
        const date = new Date(review.create_date)
        const dateString = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`

        // dateString 키 존재안할 경우 
        if (!(dateString in sortedReviews)) {
            sortedReviews[dateString] = {}
        }
        
        // foodType 배열 존재안할경우
        const foodType = review.food_type
        if (!(foodType in sortedReviews[dateString])) {
            sortedReviews[dateString][foodType] = []
        }

        sortedReviews[dateString][foodType].push(Number(review.rating))
    }

    return sortedReviews
}

export function sortReviewsByGender(reviews) {
    let sortedReviews = {}
    for (const review of reviews) {

        const foodType = review.food_type
        if (!(foodType in sortedReviews)) {
            sortedReviews[foodType] = {'M': [], 'F': []}
        }

        sortedReviews[foodType][review.author.userinfo.gender].push(review.rating)
    }

    return sortedReviews
}

export function sortReviewsByAge(reviews) {
    let sortedReviews = {}

    for (const review of reviews) {
        const birthday = new Date(review.author.userinfo.birthday)
        const today = new Date();
        const age = today.getFullYear() - birthday.getFullYear() + 1;
        const ageRange = (age - (age % 10)) + '대'

        if (!(ageRange in sortedReviews)) {
            sortedReviews[ageRange] = []
        }
        sortedReviews[ageRange].push(review)
    }
    
    return sortedReviews
}

export function makeAgeChartDataset(sortedReviews) {
    const chartLabels = Object.keys(sortedReviews).sort()
    let chartDataset = {data: [], label: chartLabels, backgroundColor: []}

    for (const key of chartLabels) {
        const arrLength = sortedReviews[key].length
        const color = randomColor(0.3)
        chartDataset.data.push(arrLength)
        chartDataset.backgroundColor.push(color)
    }

    return [chartLabels, chartDataset]
}

export function makeGenderChartDataset(sortedReviews, labelToIdx) {
    let chartDataset = {}
    const genderString = {'M': '남성', 'F': '여성'}
    const genderColor = {'M': 'rgba(85, 95, 236, 0.5)', 'F': 'rgba(236, 85, 136, 0.5)'}

    labelToIdx[-1] = '평균'
    const chartLabels = Object.values(labelToIdx)

    for (const gender of ['M', 'F']) {
        chartDataset[gender] = {data: [], label: genderString[gender], backgroundColor: genderColor[gender], borderColor: genderColor[gender]}

        for (const foodType in labelToIdx) {
            let ratingArray
            if (foodType == -1) {
                ratingArray = Object.values(sortedReviews).reduce((acc, cur) => {
                    cur = cur[gender] || []
                    return acc.concat(cur)
                }, [])
            } else {
                ratingArray = sortedReviews[foodType][gender] || []
            }
            chartDataset[gender].data.push(average(ratingArray))
        }
    }

    return [chartLabels, chartDataset]
}

export function makeDateChartDataset(sortedReviews, labelToIdx) {
    // 차트 데이터가공
    let chartDataset = {}
    const chartLabels = Object.keys(sortedReviews).sort()

    for (const foodType in labelToIdx) {
        chartDataset[foodType] = {data: [], label: labelToIdx[foodType]}

        // foodType별 평균
        for (const date of chartLabels) {
            let ratingArray

            if (foodType == -1) { // 전체평균
                ratingArray = Object.values(sortedReviews[date]).reduce((acc, cur) => acc.concat(cur), [])
                chartDataset[foodType].label = '평균'
            } else { // foodType별 평균
                ratingArray = sortedReviews[date][foodType] || []
            }
            chartDataset[foodType].data.push(average(ratingArray))
        }
    }

    return [chartLabels, chartDataset]
}