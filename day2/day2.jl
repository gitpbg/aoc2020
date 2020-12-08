
function policy1(line)
    range, ch, passwd = split(line, " ")
    minmax = split(range, "-")
    min = parse(Int64, minmax[1])
    max = parse(Int64, minmax[2])
    thech = ch[1]
    count = 0
    for i in eachindex(passwd)
        if passwd[i] == thech
            count = count + 1
        end
    end
    if count >= min && count <= max 
        return true
    end
    return false
end

function policy2(line)
    range, ch, passwd = split(line, " ")
    minmax = split(range, "-")
    min = parse(Int64, minmax[1])
    max = parse(Int64, minmax[2])
    thech = ch[1]
    count = 0
    xor(thech == passwd[min], thech == passwd[max])
end
open("input.txt", "r") do f
    goodpass = 0
    for line in eachline(f) 
        if policy2(line) 
            goodpass = goodpass + 1
        end
    end
    println("Good Passwords ", goodpass)
end