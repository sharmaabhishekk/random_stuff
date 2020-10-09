using Plots

"""
   arc(h,k,r,α, β)

       Custom function to help draw an arc of radius (r) with centre (h,k) and extending upto angles α & β. 
       Needed for the pitch arcs. 

   For example, 

       α = 0; β = 2π would give you a full circle.  
       α = 0; β = π would give you a semicircle. 

   Returns:
       arrays θ and h which are the points on the circumference of the arc defined by the parameters 
"""
function arc(h, k, r, α=0, β=2π) 
   θ = LinRange(α, β, 500) 
   h .+ r*sin.(θ), k .+ r*cos.(θ) 
end 


"""
   plot_arcs(type)

       Hackish function to draw the arcs in front of the D-box and the corners 
       type: corners/left/right

   Returns:
       nothing

"""
function plot_arcs(type, p) 
   θs = LinRange(0, 2π, 500) 
   radius = 9 
   xs = radius*cos.(θs) 
   ys = radius*sin.(θs) 
                        
   if (type == "corners")

       x_conds = [xs.>=0, xs.<=120, xs.<=120, xs.>=0] 
       y_conds = [ys.>=0, ys.>=0, ys.<=80, ys.<=80] 
       x_offsets = [0, 120, 120, 0]
       y_offsets = [0, 0, 80, 80]

       for (xcond, ycond, xoff, yoff) in zip(x_conds, y_conds, x_offsets, y_offsets)
           radius = 2
           xs = radius*cos.(θs) 
           ys = radius*sin.(θs) 

           xs = xs .+ xoff    
           ys = ys .+ yoff 
           final = (xcond) .& (ycond)
           xh = xs[1:end-1] 
           yh = ys[1:end-1] 

           plot!(p, xh, yh, color = :red)
       end    

   

   elseif(type == "left")     
           xs = xs .+ 12     
           ys = ys .+ 40 
           cond = xs.>=18 
           xh = xs[findall(cond)] 
           yh = ys[findall(cond)] 
           plot!(p, xh, yh, color = :red) 
                
   elseif(type == "right") 
           xs = xs .+ 108     
           ys = ys .+ 40 
           cond = xs.<=102 
           xh = xs[findall(cond)] 
           yh = ys[findall(cond)] 
           plot!(p, xh, yh, color = :red) 
   end 
end

"""
pitch_plot()

driver function which plots the pitch

"""
function pitch_plot()
    
    x1 = [0, 120, 120, 0, 0]; y1 = [0, 0, 80, 80, 0] ## pitch outlines 
    x2 = [0, 18, 18, 0, 0]; y2 = [18, 18, 62, 62, 18] ## left d-box 
    x3 = [102, 120, 120, 102, 102]; y3 = [18, 18, 62, 62, 18] ## right d-box 
    x4 = [0, 6, 6, 0, 0]; y4 = [30, 30, 50, 50, 30] ## left 6-yard box 
    x5 = [114, 120, 120, 114, 114]; y5 = [30, 30, 50, 50, 30] ## right 6-yard box 

    ##goals 
    x6 = [0,0]; y6 = [36, 44] 
    x7 = [120, 120]; y7=y6 

    ##halfway line and penalty spots 
    x8 = [60,60]; y8 = [0,80] 

    p = plot(x1, y1, color=:red) 
    plot!(p, x2, y2, color=:red) 
    plot!(p, x3, y3, color=:red) 
    plot!(p, x4, y4, color=:red) 
    plot!(p, x5, y5, color=:red) 
    plot!(p, x6, y6, color=:red, lw=4) 
    plot!(p, x7, y7, color=:red, lw=4) 
    plot!(p, x8, y8, color=:red) 
    plot!(p, xlim=(-1, 121), ylim=(-1, 95), legend=false, grid=false, border=:none) 
    scatter!(p, [12, 60, 108], [40, 40, 40], color=:red) 

    plot!(p, arc(60, 40, 8.5), seriestype = [:shape,], lw = 0.5, linecolor = :red, fillalpha = 0.01, aspect_ratio = 1) 

    plot_arcs("right", p) 
    plot_arcs("left", p) 
    plot_arcs("corners", p)

    p

end

# p = pitch_plot()

# gui()
# readline()


