### A Pluto.jl notebook ###
# v0.12.3

using Markdown
using InteractiveUtils

# ╔═╡ 04dbd1f0-09f3-11eb-1815-09de473d303f
begin
	using DataFrames
	using JSON
	using Statistics
	using Plots
	
	include("pitch.jl")
end	

# ╔═╡ de78be50-09f3-11eb-1999-3b25d42193ea
begin
	##Open file and plot data
	data = JSON.parsefile(raw"C:\repository\open-data\data\events\18242.json")
	team_number = 2 #1/2
	starting_players = [el["player"]["name"] for el in data[team_number]["tactics"]["lineup"]]
	team_name = data[team_number]["team"]["name"]
	
	data = filter!(e->e["type"]["name"]=="Pass", data)
end	

# ╔═╡ 39e1c660-09f4-11eb-3c7e-b7e68c2d8249
begin

	get_name(d) = d["name"]
	get_outcome(d) = haskey(d, "outcome") ? 0 : 1 
	get_recipient(d) = d["recipient"]["name"]
	get_x(array) = array[1]
	get_y(array) = array[2]
	get_value(t) = t[1]
end

# ╔═╡ e14cecf0-09f3-11eb-142f-839356f3b1ac
begin
	cols = reduce(∩, keys.(data))
	df = DataFrame((Symbol(c)=>getindex.(data, c) for c ∈ cols)...)

	df[!, "type"] = map(get_name, df[!, "type"])
	df[!, "team"] = map(get_name, df[!, "team"])
	df[!, "player"] = map(get_name, df[!, "player"])
	df[!, "outcome"] = map(get_outcome, df[!, "pass"]) ##successful passes and unsuccessful passes
	df[!, "X"] = map(get_x, df[!, "location"]) 
	df[!, "Y"] = map(get_y, df[!, "location"]) 
	
	df = df[((df[:, "outcome"] .== 1) .& (df[:, "team"] .== team_name)), :] ##get only successful passes from particular team
	df[!, "recipient"] = map(get_recipient, df[!, "pass"]); ##get recipients for successful passes
	df = df[ ([x in starting_players for x in df[:player]]) .& ([x in starting_players for x in df[:recipient]]) ,:]

	df = df[!, [:player, :recipient, :X, :Y, :minute, :second]]
end

# ╔═╡ 3d378110-09f4-11eb-0b07-aff3597fa532
begin
	grouped_df = groupby(df, [:player, :recipient])
	pass_links = combine(grouped_df, :player => size) ##important
	pass_links[!, "passes"] = map(get_value, pass_links["player_size"])
end

# ╔═╡ 194ce780-09f5-11eb-0a55-f1cee3b18fcc
pass_links

# ╔═╡ c99e5740-09ff-11eb-071c-dfe436f69207
begin
	player_df = groupby(df, :player)
	locations = combine([:X, :Y] => (x, y) -> (avg_x=mean(x), avg_y=mean(y)), player_df) ##important
	player_totals = combine(player_df, :player => size)
	player_totals[!, "total"] = map(get_value, player_totals["player_size"]) ##important

	fin = outerjoin(locations, player_totals, on = :player)
	final = outerjoin(fin, pass_links, on=:player, makeunique=true)
end

# ╔═╡ 1d8a6a20-09f5-11eb-23ec-6502a2af23cd
begin
	##draw everything
	
	p = pitch_plot()

	for row in eachrow(final)
		end_x = locations[locations["player"] .== row.recipient, "avg_x"][1]
		end_y = locations[locations["player"] .== row.recipient, "avg_y"][1]
		plot!(p, [row.avg_x, end_x], [row.avg_y, end_y], color=:blue, linewidth=row.passes/1.5, alpha=row.passes/15) 

	end
	scatter!(p, fin.avg_x, fin.avg_y, color=:gold, markersize=fin.total ./3, dpi=120)
	[annotate!(p, row.avg_x, row.avg_y, text(row.player, :blue, :left, 6)) for row in eachrow(fin)]
	annotate!(p, 60, 90, text("2015 Champions League Final", :red, :center, 14))
end	

# ╔═╡ 1eef5150-09f5-11eb-164f-bf65564ec143


# ╔═╡ Cell order:
# ╠═04dbd1f0-09f3-11eb-1815-09de473d303f
# ╠═de78be50-09f3-11eb-1999-3b25d42193ea
# ╠═39e1c660-09f4-11eb-3c7e-b7e68c2d8249
# ╠═e14cecf0-09f3-11eb-142f-839356f3b1ac
# ╠═3d378110-09f4-11eb-0b07-aff3597fa532
# ╠═194ce780-09f5-11eb-0a55-f1cee3b18fcc
# ╠═c99e5740-09ff-11eb-071c-dfe436f69207
# ╠═1d8a6a20-09f5-11eb-23ec-6502a2af23cd
# ╠═1eef5150-09f5-11eb-164f-bf65564ec143
