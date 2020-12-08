f = open("input1.txt", "r")
data = []
for l in eachline(f) 
    append!(data, parse(Int64, l))
end

function answer(data) 
    for i = 1:length(data)
        for j = i + 1:length(data) 
            if data[i] + data[j] == 2020 
                println(data[i], " ", data[j], " ", data[i] * data[j])
                return
            end
        end
    end
end

function answer2(data)
    for i = 1:length(data)
        for j = i + 1:length(data) 
            for k = i + 2:length(data)
                if data[i] + data[j] + data[k] == 2020 
                    println(data[i], " ", data[j], " ", data[k], " ", data[i] * data[j] * data[k])
                    return
                end
            end
        end
    end
end

answer(data)
answer2(data)