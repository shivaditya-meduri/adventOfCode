def process_input(inp):
    out = []
    file_id = 0
    for i, c in enumerate(inp):
        if i%2==0:
            out.extend([str(file_id)]*int(c))
            file_id += 1
        else:
            out.extend(["."]*int(c))
    return out

def calc_checksum(inp):
    # Will not work for > 1 digit file IDs
    out = 0
    for i, c in enumerate(inp):
        if c==".":
            continue
        else:
            out += int(c)*i
    return out
  
def sol1_2pointers(inp):
  p1, p2 = 0, len(inp)-1
  while p1<p2:
      if inp[p1]=="." and inp[p2]!=".":
          inp[p1], inp[p2] = inp[p2], inp[p1]
          p1 += 1
          p2 -= 1
      elif inp[p1]!=".":
          p1 +=1
      elif inp[p2]==".":
          p2 -= 1
  return calc_checksum(inp)
test_input = "2333133121414131402"
print(sol1_2pointers(process_input(test_input)))

# Solution part 2
def process_inp_2(inp):
    file_blocks, empty_space = [], []
    file_id = 0
    for i, c in enumerate(inp):
        if i%2 == 0:
            file_blocks.append([file_id, int(c)])
            file_id += 1
        else:
            empty_space.append(int(c))
    empty_space.append(0)
    return file_blocks, empty_space

def find_file(file_id, file_blocks):
    for f_i, (file_id_i, file_size) in enumerate(file_blocks):
        if file_id_i == file_id:
            return f_i
            
def sol2_bruteforce(file_blocks, empty_space):
    max_file_id = len(file_blocks)-1
    for file_id in range(max_file_id, -1, -1):
        file_index = find_file(file_id, file_blocks)
        file_size = file_blocks[file_index][1]
        for ei in range(file_index):
            if empty_space[ei] >= file_size:
                file_blocks.insert(ei+1, file_blocks.pop(file_index))
                empty_space.insert(ei, 0)
                empty_space[ei+1] -= file_size
                eLast = empty_space.pop(file_index+1)
                empty_space[file_index] += eLast + file_size
                break
    return file_blocks, empty_space        

def calc_checksum_2(file_blocks, empty_space):
    # Can handle multi digit File IDs
    out = 0
    ind = 0
    for file_ind, (file_id, file_size) in enumerate(file_blocks):
        for _ in range(file_size):
            out += file_id*ind
            ind += 1
        ind += empty_space[file_ind]
    return out

file_blocks, empty_space = process_inp_2(test_input)
file_blocks, empty_space = sol2_bruteforce(file_blocks, empty_space)
print(calc_checksum_2(file_blocks, empty_space))
