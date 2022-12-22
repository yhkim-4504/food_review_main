'use strict'

import * as chartUtils from './chartUtils.js'

document.addEventListener("DOMContentLoaded", function() {
    // Variables
    const ctx = document.getElementById('chart')
    let myChart = new Chart(ctx)

    $("#submit").click(function() {
        // json 형식으로 데이터 set
        const params = {
            startdate: $('#startdate').val(),
            enddate: $('#enddate').val(),
            analysis_type: $("input:radio[name='analysis_type']:checked").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
            
        // ajax 통신
        $.ajax({
            type : "POST",
            url : "",
            data : params,
            success : function(res) {
                const errorDiv = document.getElementById('error')
                errorDiv.innerHTML = ''

                // form error 발생시
                if (res.form_error) {
                    for (const label in res.field) {
                        const newError = document.createElement('div')
                        const fieldErrorList = res.field[label].reduce((acc, cur) => acc + `<li>${cur}</li>`, '')
                        newError.innerHTML = `<ul><strong>${label}</strong>${fieldErrorList}</ul>`
                        errorDiv.appendChild(newError)
                    }

                    for (const error of res.non_field) {
                        const newError = document.createElement('div')
                        newError.innerHTML = `<strong>${error}</strong>`
                        errorDiv.appendChild(newError)
                    }

                    return false
                }

                let labelToIdx = res.idx2label
                const reviews = res.reviews
                
                if (reviews.length == 0) {
                    alert('해당 기간에 리뷰가 존재하지 않습니다.\n기간을 다시 선택해주세요.')
                    return false
                }
                
                if (params.analysis_type == 'total') {
                    // Total
                    const sortedReviews = chartUtils.sortReviewsByDate(reviews)
                    const [chartLabels, chartDataset] = chartUtils.makeDateChartDataset(sortedReviews, labelToIdx)
                    myChart = chartUtils.drawChart(chartLabels, chartDataset, 'line', '날짜별 리뷰평점 분석차트', ctx, myChart)
                } else if (params.analysis_type == 'gender') {
                    // Gender
                    const sortedReviews = chartUtils.sortReviewsByGender(reviews)
                    const [chartLabels, chartDataset] = chartUtils.makeGenderChartDataset(sortedReviews, labelToIdx)
                    myChart = chartUtils.drawChart(chartLabels, chartDataset, 'bar', '남녀별 리뷰평점 분석차트', ctx, myChart)
                } else if (params.analysis_type == 'age') {
                    // Age
                    const sortedReviews = chartUtils.sortReviewsByAge(reviews)
                    const [chartLabels, chartDataset] = chartUtils.makeAgeChartDataset(sortedReviews)
                    const totalOrderNum = chartDataset.data.reduce((acc, cur) => acc+cur, 0)
                    myChart = chartUtils.drawChart(chartLabels, [chartDataset], 'pie', `나이대별 주문수 분석 - 총 주문수 : ${totalOrderNum}건`, ctx, myChart, {})
                } else {
                    alert(`존재하지 않는 분석타입입니다. - ${params.analysis_type}`)
                }

                return true
            },
            error: function(request, status, error) {
                alert('Connection Error!')
                console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error)
            }
        })
    })
})
