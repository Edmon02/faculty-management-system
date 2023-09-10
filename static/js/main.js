"use strict";

function qs(selector, all = false) {
  return all ? document.querySelectorAll(selector) : document.querySelector(selector);
}
     
const navLinks = document.getElementById("navLinks");
const sections = qs('.section', true);
const timeline = qs('.timeline');
const line = qs('.line');
line.style.bottom = `calc(100% - 20px)`;
let prevScrollY = window.scrollY;
let up, down;
let full = false;
let set = 0;
const targetY = window.innerHeight * .8;




const wrapper = document.querySelector('.login-wrapper');
const btnPopup = document.querySelector('.login-btn');
const iconClose = document.querySelector('.icon-close'); 

btnPopup.addEventListener( 'click' , () => {
  wrapper.classList.toggle('active-popup')
});

iconClose.addEventListener( 'click' , () => {
  wrapper.classList.remove('active-popup')
});

function showMenu(){
  navLinks.style.right = '0';
}

function hideMenu(){
  navLinks.style.right = '-100%';
}
     
     function scrollHandler(e) {
       const {
         scrollY
       } = window;
       up = scrollY < prevScrollY;
       down = !up;
       const timelineRect = timeline.getBoundingClientRect();
       const lineRect = line.getBoundingClientRect(); // const lineHeight = lineRect.bottom - lineRect.top;
     
       const dist = targetY - timelineRect.top;
       console.log(dist);
     
       if (down && !full) {
         set = Math.max(set, dist);
         line.style.bottom = `calc(100% - ${set}px)`;
       }
     
       if (dist > timeline.offsetHeight + 50 && !full) {
         full = true;
         line.style.bottom = `-50px`;
       }
     
       sections.forEach(item => {
         // console.log(item);
         const rect = item.getBoundingClientRect(); //     console.log(rect);
     
         if (rect.top + item.offsetHeight / 5 < targetY) {
           item.classList.add('show-me');
         }
       }); // console.log(up, down);
     
       prevScrollY = window.scrollY;
     }
     
scrollHandler();
line.style.display = 'block';
     window.addEventListener('scroll', scrollHandler);
     



// about section
const ml_section = document.querySelector(".milestone");
const ml_counters = document.querySelectorAll(".number span");


window.addEventListener("scroll" , () => {
        if(!mlPlayed) mlCounters();
})

function hasReached(el){
    let topPosition = el.getBoundingClientRect().top;
   
   if( window.innerHeight >= topPosition + el.offsetHeight ) return true;
    return false;
    
}

function updateCount( num , maxNum){
    let currentNum = +num.innerText;
    
    if( currentNum < maxNum){
        num.innerText = currentNum + 1;
        setTimeout( () => {
            updateCount(num , maxNum)
        }, 13)
    }
}

// services counter animation 

let mlPlayed = false;

function mlCounters(){
    if(!hasReached(ml_section)) return;
		mlPlayed = true;
		
    ml_counters.forEach(ctr => {
        let target = +ctr.dataset.target;

        setTimeout( () => {
            updateCount(ctr, target );
        }, 400);
    });
}
