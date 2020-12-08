function readdata(filename)
    data = []
  
    width = 0
    height = 0
    open(filename, "r") do f
        for line in eachline(f)
            for idx in eachindex(line)
                ch = line[idx]
                if (height == 0) 
                    width = width + 1
                end
                if (ch == '.')
                    append!(data, 0)
                elseif (ch == '#')
                    append!(data, 1)
                end
            end
            height = height + 1
        end
    end
#    println(data) 
    println(width, "x", height)
    transpose(reshape(data, (width, height)))
end
function calctrees(data, sx, sy, dx, dy)
    (rows, cols) = size(data)
    ox = sx
    oy = sy
    count = 0
    while oy <= rows
        count = count + data[oy, 1 + (ox - 1) % cols]
        ox = ox + dx
        oy = oy + dy
    end
    count
end

function main()
    data = readdata("input.txt")
    (rows, cols) = size(data)
    println("Rows $rows Columns $cols")
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    answer = 1
    for (dx, dy) in slopes
        count = calctrees(data, 1, 1, dx, dy)
        println("$count trees for $dx, $dy")
        answer = answer * count
    end
    println("Cumulative Product = $answer")
end

main()