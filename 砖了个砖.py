import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import heapq


def get_all_moves(board, costs=None):
    #获取所有可能的移动
    moves = []
    n = board.shape[0]

    for i in range(n):
        for j in range(n):
            if board[i,j] == 0:
                continue
            if board[i,j] != 0:
                fruit = board[i,j]
                cost = costs[fruit-1] if costs else 1
                if i > 0 and board[i-1,j] == 0:
                    moves.append(((i,j),(i-1,j), cost))
                if i < n-1 and board[i+1,j] == 0:
                    moves.append(((i,j),(i+1,j), cost))
                if j > 0 and board[i,j-1] == 0:
                    moves.append(((i,j),(i,j-1), cost))
                if j < n-1 and board[i,j+1] == 0:
                    moves.append(((i,j),(i,j+1), cost))
    return moves

def eliminate(board):
    n = board.shape[0]
    for i in range(1, np.max(board)+1):
        positions = np.argwhere(board == i)
        if len(positions) != 2:
            continue  
        (x1, y1), (x2, y2) = positions
        # 同一行
        if x1 == x2:
            added = np.sum(board[x1, min(y1, y2):max(y1, y2)+1])
            if added == i*2:
                board[x1, y1] = 0
                board[x2, y2] = 0
        # 同一列
        elif y1 == y2:
            added = np.sum(board[min(x1, x2):max(x1, x2)+1, y1])
            if added == i*2:
                board[x1, y1] = 0
                board[x2, y2] = 0
    return board

class Node():
    def __init__(self, state, parent, move, path_cost, custom_costs=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.path_cost = path_cost
        self._heuristic_value = None  # 缓存启发值
        self.custom_costs = custom_costs

    def __lt__(self, other):
        # 支持优先队列比较，f值小的优先
        return self.heuristic() < other.heuristic()

    def expand(self):
        #扩展节点，生成子节点
        children = []
        for move in get_all_moves(self.state, costs=self.custom_costs):
            new_state = self.state.copy()
            (x1,y1), (x2,y2), c1 = move
            new_state[x2,y2], new_state[x1,y1] = new_state[x1,y1], new_state[x2,y2]
            new_state = eliminate(new_state)                   
            child_node = Node(new_state, self, move, self.path_cost + c1, custom_costs=self.custom_costs)
            children.append(child_node)
        return children

    def heuristic(self, costs=None):
        #评价函数，估计到达目标状态的代价+路径代价
        board = self.state
        if np.all(board == 0):
            self._heuristic_value = self.path_cost
            return self._heuristic_value
        
        # 使用节点的自定义代价，如果没有则使用传入的costs，最后默认为1    
        use_costs = self.custom_costs if self.custom_costs else costs
            
        fruit_types = int(np.max(board))
        h = 0
        for i in range(1, fruit_types+1):
            positions = np.argwhere(board == i)
            if len(positions) == 2:
                (x1, y1), (x2, y2) = positions
                h += min(abs(x1 - x2), abs(y1 - y2)) * (use_costs[i-1] if use_costs else 1)
        
        self._heuristic_value = h + self.path_cost
        return self._heuristic_value

def A_star(board, costs=None):
    eliminate(board)
    start_node = Node(np.array(board), None, None, 0, custom_costs=costs)

    open_heap = []
    heapq.heappush(open_heap, start_node)
    
    closed_set = set()
    open_set = set()  
    
    start_state_hash = hash(tuple(start_node.state.flatten()))
    open_set.add(start_state_hash)
    
    while open_heap:
        current_node = heapq.heappop(open_heap)
        current_state_hash = hash(tuple(current_node.state.flatten()))
        open_set.discard(current_state_hash)

        if current_state_hash in closed_set:
            continue
        closed_set.add(current_state_hash)
        
        if np.all(current_node.state == 0):
            return current_node
            
        for child in current_node.expand():
            child_state_hash = hash(tuple(child.state.flatten()))
            
            if child_state_hash not in closed_set and child_state_hash not in open_set:
                heapq.heappush(open_heap, child)
                open_set.add(child_state_hash)
                
    return 'No solution found'



class FruitBoardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("砖了个砖")
        self.center_window(self.root, 900, 900)

        self.board_size = None
        self.fruit_count = None 
        self.mode = None
        self.board = []
        self.buttons = []
        self.fruit_images = {}
        self.current_fruit = 1
        self.fruit_placed = 0
        self.custom_costs = None
        self.setup_menu()

        self.is_solving = False
        self.animation_speed = 500  

    def center_window(self, window, width, height):
        """将窗口居中显示"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")  

    def setup_menu(self):
        """初始菜单界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="选择棋盘大小：").grid(row=0, column=0, sticky="w")
        self.size_var = tk.StringVar(value="4x4")
        ttk.OptionMenu(frame, self.size_var, "4x4", "4x4", "5x5", "6x6", "7x7", "8x8").grid(row=0, column=1)

        ttk.Label(frame, text="选择水果种类数量：").grid(row=1, column=0, sticky="w")
        self.fruit_var = tk.IntVar(value=3)
        ttk.OptionMenu(frame, self.fruit_var, 3, 1, 2, 3, 4, 5).grid(row=1, column=1)

        ttk.Label(frame, text="选择摆放方式：").grid(row=2, column=0, sticky="w")
        self.mode_var = tk.StringVar(value="随机摆放")
        ttk.OptionMenu(frame, self.mode_var, "随机摆放", "手动摆放").grid(row=2, column=1)

        ttk.Label(frame, text="是否自定义滑动代价：").grid(row=3, column=0, sticky="w")
        ttk.Button(frame, text="是",command=self.customize_cost).grid(row=3, column=1, sticky="w")
        ttk.Button(frame, text="否",command=self.commands).grid(row=3, column=2, sticky="w")

    def commands(self):
        """执行多个命令的函数"""
        self.custom_costs = [1] * self.fruit_var.get()  # 默认代价为1
        self.start_game()    

    def customize_cost(self):
        """自定义滑动代价界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="请输入每种水果的滑动代价（用逗号分隔）：").grid(row=0, column=0, sticky="w")
        self.cost_entry = ttk.Entry(frame, width=30)
        self.cost_entry.grid(row=0, column=1)

        ttk.Button(frame, text="确认", command=self.parse_and_start_game).grid(row=1, column=0, columnspan=2, pady=10)

    def parse_and_start_game(self):
        """解析用户输入的代价并开始游戏"""
        costs_input = self.cost_entry.get().strip()
        if not costs_input:
            messagebox.showerror("错误", "请输入代价值")
            return
        
        costs = costs_input.split(',')
        try:
            self.custom_costs = [int(cost.strip()) for cost in costs]
            if len(self.custom_costs) != self.fruit_var.get():
                messagebox.showerror("错误", f"需要输入{self.fruit_var.get()}个代价值，当前输入了{len(self.custom_costs)}个")
                return
            self.start_game()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数代价，用逗号分隔")
            return

    def start_game(self):
        """根据选择创建棋盘"""
        size_text = self.size_var.get()
        self.board_size = int(size_text[0])
        self.fruit_count = self.fruit_var.get()
        self.mode = self.mode_var.get()
        self.board = [[0] * self.board_size for _ in range(self.board_size)]

        self.load_images()
        self.draw_board()

        if self.mode == "随机摆放":
            self.random_place_fruits()
            self.show_board()

    def load_images(self):
        """加载水果图像"""
        self.fruit_images = {}
        for i in range(1, self.fruit_count + 1):
            try:
                img = tk.PhotoImage(file=f"fruit{i}.png")
                self.fruit_images[i] = img
            except Exception as e:
                messagebox.showwarning("警告", f"无法加载 fruit{i}.png: {e}\n将使用默认图像")
                self.fruit_images[i] = None
            
    def draw_board(self):
        """绘制棋盘"""
        for widget in self.root.winfo_children():
            widget.destroy()

        top = ttk.Frame(self.root, padding=10)
        top.pack()
        ttk.Label(top, text=f"棋盘大小：{self.board_size}x{self.board_size} | 水果种类：{self.fruit_count} | 模式：{self.mode}").pack()
        
        # 显示水果代价信息
        if self.custom_costs:
            cost_info = "水果代价: " + ", ".join([f"水果{i+1}({self.custom_costs[i]})" for i in range(len(self.custom_costs))])
            ttk.Label(top, text=cost_info, foreground="blue").pack()
        
        if self.mode == "手动摆放":
            ttk.Label(top, text="同种水果放置两个后会自动切换下一种水果").pack(pady=5)

        # 添加求解按钮
        ttk.Button(top, text="求解并显示路径", command=self.solve_and_show_path).pack(pady=5)

        board_frame = ttk.Frame(self.root)
        board_frame.pack()

        try:
            self.placeholder = tk.PhotoImage(file="button.png")
        except Exception:

            self.placeholder = tk.PhotoImage(width=64, height=64)

        self.buttons = []
        for r in range(self.board_size):
            row = []
            for c in range(self.board_size):
                btn = tk.Button(board_frame,
                                relief='solid', borderwidth=1,
                                padx=0, pady=0,
                                image=self.placeholder,
                                command=lambda r=r, c=c: self.place_fruit(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.image = self.placeholder  
                row.append(btn)
            self.buttons.append(row)

    def place_fruit(self, r, c):
        """手动摆放水果"""
        if self.mode != "手动摆放":
            return

        if self.board[r][c] != 0:
            messagebox.showinfo("提示", "这个格子已经放过水果了！")
            return

        if self.current_fruit > self.fruit_count:
            messagebox.showinfo("完成", "所有水果都已放置完毕！")
            return

        self.board[r][c] = self.current_fruit
        if self.fruit_images[self.current_fruit]:
            img = self.fruit_images[self.current_fruit]
            self.buttons[r][c].config(image=img)
            self.buttons[r][c].image = img

        self.fruit_placed += 1
        if self.fruit_placed % 2 == 0:
            self.current_fruit += 1

        if self.current_fruit > self.fruit_count:
            messagebox.showinfo("完成", "所有水果都已放置完毕！")
            print("最终方阵：")
            for row in self.board:
                print(row)

    def random_place_fruits(self):
        """随机摆放水果"""
        positions = [(r, c) for r in range(self.board_size) for c in range(self.board_size)]
        random.shuffle(positions)

        needed = self.fruit_count * 2
        if needed > len(positions):
            messagebox.showerror("错误", "棋盘太小，放不下所有水果！")
            return

        idx = 0
        for i in range(1, self.fruit_count + 1):
            for _ in range(2):
                r, c = positions[idx]
                idx += 1
                self.board[r][c] = i

    def show_board(self):
        """显示随机摆放结果"""
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] != 0 and self.fruit_images[self.board[r][c]]:
                    img = self.fruit_images[self.board[r][c]]
                    self.buttons[r][c].config(image=img)
                    self.buttons[r][c].image = img

        print("随机摆放方阵：")
        for row in self.board:
            print(row)

    def solve_and_show_path(self):
        """求解并在当前棋盘上显示路径"""
        if self.is_solving:
            messagebox.showinfo("提示", "正在求解中，请稍等...")
            return
        
        self.is_solving = True
        
        board_copy = np.array(self.board)
        result = A_star(board_copy, costs=self.custom_costs)
        
        if result == 'No solution found':
            messagebox.showinfo("结果", "未找到解决方案")
            self.is_solving = False
            return
        
        # 重建移动序列
        moves = []
        total_cost = 0
        node = result
        while node.parent is not None:
            moves.append(node.move)
            total_cost += node.move[2]  # 累计代价
            node = node.parent
        moves.reverse()
        
        # 在控制台显示
        print("Moves to solve the board:")
        for i, move in enumerate(moves):
            print(f"第{i+1}步: {move} (代价: {move[2]})")
        print(f"总代价: {total_cost}")
        
        # 在当前棋盘上可视化路径
        self.visualize_path_on_board(moves)
        
        self.is_solving = False

    def visualize_path_on_board(self, moves):
        """在当前棋盘上可视化路径"""
        self.original_board = [row[:] for row in self.board]
        self.moves_list = moves
        self.current_move_index = 0
        
        if not hasattr(self, 'control_frame') or not self.control_frame.winfo_exists():
            self.create_control_buttons()
        
        self.update_status_label(f"找到解决方案！共 {len(moves)} 步。点击'下一步'开始演示")

    def create_control_buttons(self):
        """创建控制按钮"""
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=10)
        
        self.status_label = ttk.Label(self.control_frame, text="", 
                                     font=('Arial', 11))
        self.status_label.pack(pady=(0, 5))
        
        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack()
        
        self.prev_btn = ttk.Button(button_frame, text="上一步", 
                                  command=self.show_previous_step, state='disabled')
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(button_frame, text="下一步", 
                                  command=self.show_next_step)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_btn = ttk.Button(button_frame, text="自动演示", 
                                  command=self.auto_play)
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(button_frame, text="重置", 
                                   command=self.reset_visualization)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def show_next_step(self):
        """显示下一步移动"""
        if not hasattr(self, 'moves_list') or self.current_move_index >= len(self.moves_list):
            return
        
        move = self.moves_list[self.current_move_index]
        (start_r, start_c), (end_r, end_c), cost = move
        
        old_board = [row[:] for row in self.board]
        self.highlight_move(start_r, start_c, end_r, end_c)
        self.board[end_r][end_c] = self.board[start_r][start_c]
        self.board[start_r][start_c] = 0
        
        board_array = np.array(self.board)
        board_array = eliminate(board_array)
        self.board = board_array.tolist()
        
        self.update_changed_cells(old_board, self.board)
        self.current_move_index += 1
        fruit_type = self.board[end_r][end_c] if hasattr(self, 'original_board') and self.original_board[start_r][start_c] != 0 else "未知"
        if hasattr(self, 'original_board') and self.original_board[start_r][start_c] != 0:
            fruit_type = self.original_board[start_r][start_c]
        self.update_status_label(f"第 {self.current_move_index} 步: 水果{fruit_type} 从 ({start_r},{start_c}) 到 ({end_r},{end_c}), 代价: {cost}")
        
        self.prev_btn.config(state='normal')
        if self.current_move_index >= len(self.moves_list):
            self.next_btn.config(state='disabled')
            total_cost = sum([move[2] for move in self.moves_list])
            self.update_status_label(f"✅ 演示完成！所有水果已消除，总代价: {total_cost}")

    def show_previous_step(self):
        """显示上一步（重建到上一状态）"""
        if self.current_move_index <= 0:
            return
        
        self.rebuild_board_to_step(self.current_move_index - 1)
        
        self.current_move_index -= 1
        if self.current_move_index == 0:
            self.prev_btn.config(state='disabled')
            self.update_status_label("回到初始状态")
        else:
            move = self.moves_list[self.current_move_index - 1]
            (start_r, start_c), (end_r, end_c) = move
            self.update_status_label(f"第 {self.current_move_index} 步: 从 ({start_r},{start_c}) 到 ({end_r},{end_c})")
        
        self.next_btn.config(state='normal')

    def rebuild_board_to_step(self, step):
        """重建棋盘状态到指定步骤"""
        old_board = [row[:] for row in self.board]
        self.board = [row[:] for row in self.original_board]
        
        for i in range(step):
            move = self.moves_list[i]
            (start_r, start_c), (end_r, end_c),cost = move
            
            self.board[end_r][end_c] = self.board[start_r][start_c]
            self.board[start_r][start_c] = 0
            
            board_array = np.array(self.board)
            board_array = eliminate(board_array)
            self.board = board_array.tolist()
        
        self.update_changed_cells(old_board, self.board)

    def highlight_move(self, start_r, start_c, end_r, end_c):
        """高亮显示移动的起点和终点"""
        self.clear_highlights()
        self.buttons[start_r][start_c].config(relief='solid', borderwidth=3, 
                                             highlightbackground='orange', highlightcolor='orange')
        self.buttons[end_r][end_c].config(relief='solid', borderwidth=3,
                                         highlightbackground='lime', highlightcolor='lime')

    def clear_highlights(self):
        """清除所有高亮"""
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.buttons[r][c].config(relief='solid', borderwidth=1,
                                        highlightbackground='SystemButtonFace', highlightcolor='SystemButtonFace')

    def update_board_display(self):
        """更新棋盘显示"""
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] != 0 and self.fruit_images.get(self.board[r][c]):
                    img = self.fruit_images[self.board[r][c]]
                    self.buttons[r][c].config(image=img)
                    self.buttons[r][c].image = img
                else:
                    self.buttons[r][c].config(image=self.placeholder)
                    self.buttons[r][c].image = self.placeholder

    def update_changed_cells(self, old_board, new_board):
        """只更新发生变化的格子，提高效率"""
        for r in range(self.board_size):
            for c in range(self.board_size):
                if old_board[r][c] != new_board[r][c]:
                    self.update_single_cell(r, c, new_board[r][c])

    def update_single_cell(self, row, col, value):
        """更新单个格子的显示"""
        if value != 0 and self.fruit_images.get(value):
            img = self.fruit_images[value]
            self.buttons[row][col].config(image=img)
            self.buttons[row][col].image = img
        else:
            self.buttons[row][col].config(image=self.placeholder)
            self.buttons[row][col].image = self.placeholder

    def auto_play(self):
        """自动播放演示"""
        if hasattr(self, 'moves_list') and self.current_move_index < len(self.moves_list):
            self.show_next_step()
            self.root.after(300, self.auto_play)

    def reset_visualization(self):
        """重置可视化"""
        if hasattr(self, 'original_board'):
            self.board = [row[:] for row in self.original_board]
            self.current_move_index = 0
            self.clear_highlights()
            self.update_board_display()
            self.prev_btn.config(state='disabled')
            self.next_btn.config(state='normal')
            self.update_status_label("重置完成，点击'下一步'开始演示")

    def update_status_label(self, text):
        """更新状态标签"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = FruitBoardApp(root)
    root.mainloop()

    board = np.array(app.board)
    costs = app.custom_costs
    result = A_star(board, costs)
    if result != 'No solution found':
        moves = []
        node = result
        while node.parent is not None:
            moves.append(node.move)
            node = node.parent
        moves.reverse()
        print("Moves to solve the board:")
        for move in moves:
            print(move)
    else:
        print(result)