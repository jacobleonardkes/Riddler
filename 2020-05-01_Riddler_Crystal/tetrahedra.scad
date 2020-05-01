
module plotSteps(steps)
{
for(z = [0:steps])
{
    translate([-100*(1-(z/steps))/2,-100*z/(2*steps),100*z/steps])
        cube([100*(1-z/steps),0.01+100*z/steps,100*(1/steps)]);
}
}

plotSteps(1000);
translate([0,100,0])
    plotSteps(10);