// 成绩导出表单验证
function initExportForm() {
    $('form').on('submit', function(e) {
        if ($('input[name="fields"]:checked').length === 0) {
            e.preventDefault();
            alert('请至少选择一个导出字段！');
        }
    });
}

// 初始化成绩分布图表
function initGradeDistributionChart(gradeDistribution) {
    var ctx = document.getElementById('gradeDistributionChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(gradeDistribution),
            datasets: [{
                label: '学生人数',
                data: Object.values(gradeDistribution),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '成绩分布统计'
                }
            }
        }
    });
}

// 页面加载完成后初始化
$(document).ready(function() {
    initExportForm();
    // 注意：gradeDistribution将在HTML中通过模板变量传入
}); 