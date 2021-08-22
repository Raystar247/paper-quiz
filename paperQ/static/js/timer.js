console.log(finishUri);
console.log(time);
displayRestTime( Math.floor(time/60), time%60 );
// setTimeout(redirect, time*1000);
setInterval(count, 1000)

function redirect() {
    console.log("転送されました");
    location.href=finishUri;
}

function zeroPadding(num,length) {
    return ('00' + num).slice(-length);
}

function displayRestTime(minutes, seconds) {
    minutesStr = zeroPadding(minutes, 2);
    secondsStr = zeroPadding(seconds, 2);
    let timeString = minutesStr + ":" + secondsStr;
    $('#timeDisplay').text(timeString);
}

function count() {
    if (time == 0) {
        redirect();
    }
    displayRestTime( Math.floor(time/60), time%60 );
    time --;
}