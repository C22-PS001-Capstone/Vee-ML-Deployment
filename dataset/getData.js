const fs = require("fs")
const moment = require("moment")

const initDate = moment(new Date(2019, 0, 1, 7))
const uniqueDate = [
    // Eid 2019
    [moment("28/05/2019", "DD/MM/YYYY").unix(), moment("08/06/2019", "DD/MM/YYYY").unix()],
    // Christmast 2019
    [moment("24/12/2019", "DD/MM/YYYY").unix(), moment("26/12/2019", "DD/MM/YYYY").unix()],
    // PPKM 1
    [moment("11/01/2021", "DD/MM/YYYY").unix(), moment("25/01/2021", "DD/MM/YYYY").unix()],
    // PPKM Darurat
    [moment("03/07/2021", "DD/MM/YYYY").unix(), moment("20/07/2021", "DD/MM/YYYY").unix()],
    // Eid and Christmas not available
]
// Price fuel pertamax
// Price fuel per liter 2019 https://www.liputan6.com/bisnis/read/4100829/Price-fuel-pertamina-shell-dan-total-awal-november-2019-mana-termurah#:~:text=%E2%80%8EBerdasarkan%20pantauan%20Price%20fuel,dijual%20Rp%2011.200%20per%20liter.
// 1 september 
let perLitre2019 = 9850
// 1 februari 2020 https://www.pertamina.com/id/news-room/announcement/daftar-Price-bbk-tmt-01-februari-2020
let perLitre2020 = 9000
let perLitre = perLitre2019

// Full tank 58L
let rataRataLiter = 25

const dataSet = []

let randomDay = 0

do {
    const random = Math.floor(Math.random() * 9) + 1
    let randomUsed = Math.floor(Math.random() * 10) + 1
    let randomPrice = (rataRataLiter + randomUsed) * perLitre
    if(initDate.unix() >= uniqueDate[0][0] && initDate.unix() <= uniqueDate[0][1] || initDate.unix() >= uniqueDate[1][0] && initDate.unix() <= uniqueDate[1][1]){
        if(random > 2){
            const dateSet = initDate.format("YYYY-MM-DD")
            const cost = randomPrice
            dataSet.push({
                date: dateSet,
                cost: cost
            })
        }
    } else {
        if(randomDay == initDate.day()){
            var cost = randomPrice
            if(initDate.unix() >= uniqueDate[2][0] && initDate.unix() <= uniqueDate[2][1]){
                const minus = Math.floor(Math.random() * (cost*0.5)/1000)*1000 + 1
                cost = cost - minus
            }
            if(initDate.unix() >= uniqueDate[3][0] && initDate.unix() <= uniqueDate[3][1]){
                const minus = Math.floor(Math.random() * (cost*0.8)/1000)*1000 + 1
                cost = cost - minus
            }
            const dateSet = initDate.format("YYYY-MM-DD")
            dataSet.push({
                date: dateSet,
                cost: cost
            })
            randomDay = Math.floor(Math.random() * 6)
        }
    }
    if(initDate.unix() > moment("01/02/2020", "DD/MM/YYYY").unix()){
        perLitre = perLitre2020
    }
    initDate.add(1, "day")
} while(initDate.unix() <= moment(new Date(2022, 0, 1, 7)).unix())
console.log(dataSet)

const csvString = [
    [
        "date",
        "cost"
    ],
    ...dataSet.map(data => [
        data.date,
        data.cost
    ])
].map(data => data.join(",")).join("\n")

fs.writeFileSync("./data.csv", csvString)