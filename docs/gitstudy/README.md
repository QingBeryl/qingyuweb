# Git使用教程

---

## 一、Git安装配置

### 1. Git下载安装

在Windows上使用Git，可以从Git官网直接下载安装程序，然后按默认选项安装即可。

```
https://git-scm.com/install/
```

桌面右键出现如下选项即为安装成功。

![image-20260624192307158](static/docs/Git使用教程/images/image-20260624192307158.png)

说明：

- Git GUI：Git提供的图形界面工具；
- Git Bash：Git提供的命令行工具。

### 2. Git的配置

安装完毕后，我们需要提供姓名及邮箱，来让Git确保每次用户操作都能落实到人。 如果不设置，某些涉及到用户的行为就无法完成。 类似于，淘宝上可以浏览列表页，一旦要买东西，就必须要登录。

打开Bash，按照以下命令执行（用户名与邮箱更换为自己的）。

- 设置用户名称 ；

  ```bash
  git config --global user.name "QingBeryl"
  ```

- 设置用户邮箱   邮箱设置可以任意，没有邮箱校验；

  ```bash
  git config --global user.email "QingBeryl@163.com"
  ```

- 查看配置信息。

  ```bash
  git config --global user.name
  git config --global user.email
  ```

事实上，Git的配置信息，都会保存在：C:\Users\用户`.gitconfig`。

### 3. 指令简化

有些常用的指令参数非常多，每次都要输入好多参数，我们可以使用别名。 

1. 打开用户目录，创建.bashrc文件  部分windows系统不允许用户创建点号开头的文件，可以打开gitBash,执行touch ~/.bashrc ；

2. 在.bashrc文件中输入如下内容；

   ```bash
   # 声明   简化名 =  简化命令
   alias git-log='git log --pretty=oneline --abbrev-commit --all --graph --decorate'
   ```
   
3. 打开gitBash，执行以下代码使配置生效。

   ```
   source ~/.bashrc
   ```

### 4. 乱码解决

1. 打开GitBash执行下面命令；

   ```bash
   git config --global core.quotepath false
   ```

2. `${git home}/etc/bash.bashrc` 文件最后加入下面两行。

   ```bash
   export LANG="zh_CN.UTF-8"
   export LC_ALL="zh_CN.UTF-8"
   ```

---

## 二、获取本地仓库

要使用Git对我们的代码进行版本控制，首先需要初始化本地仓库。

1. 在电脑的任意位置创建一个空目录（非空也行），作为我们的本地Git仓库；

2. 进入这个仓库，右键选择Git Bash打开；

3. 执行以下命令初始化本地仓库；

   ```bash
   gti init
   ```

   如图所示即可：

   ![image-20260625163422113](static/docs/Git使用教程/images/image-20260625163422113.png)

4. 如图所示，在文件夹中可以看到一个`.git`文件夹即为初始化成功。

   ![image-20260625163512635](static/docs/Git使用教程/images/image-20260625163512635.png)

---

## 三、基础操作指令

Git工作目录下对于文件的**修改**（增加、删除、修改）会存在几个状态，这些修改会随着我们执行Git命令而发生变化。

说明：Git工作目录指文件夹中除`.git`文件夹中的内容外的所以内容。

![image-20260625164534096](static/docs/Git使用教程/images/image-20260625164534096.png)

### 1. 查看文件状态

可以使用如下命令来查看文件的状态。

```bash
git status
```

如图所示为文件的三种状态（untracked、unstaged、staged）：

![image-20260625165651866](static/docs/Git使用教程/images/image-20260625165651866.png)

如图所示即是所有文件都已提交到本地仓库：



### 2. 工作区到暂存区

我们可以使用如下命令将指定文件由工作区添加到暂存区。

```bash
git add 文件名
```

或者也可以使用下面的命令将工作区未跟踪和未暂存的所有文件全部添加到暂存区。

```bash
git add .
```

如图所示，运行命令后如没有报错，即为成功，同时可以使用查看文件状态命令检查是否成功。

![image-20260625170443926](static/docs/Git使用教程/images/image-20260625170443926.png)

### 3. 暂存区到本地仓库

文件添加到暂存区后，即可通过如下命令提交到本地仓库，形成一次提交记录；

```bash
git commit -m 注释
```

或者可以去掉`-m 注释`直接提交，则会打开vi编辑器，可在其中输入注释，适用于注释很长的情况。

```
git commit
```

注释即为每次提交的解释说明，方便团队或个人辨别每次提交的内容，英文与中文都可；此处命令注释不能为空，若需要注释为空这需要使用如下的**强制提交**命令，但会导致提交信息模糊，团队协作时难以追溯改动，仅适用于本地临时草稿提交。

```bash
git commit --allow-empty-message -m ""
```

如图所示即为提交成功：

![image-20260625171151544](static/docs/Git使用教程/images/image-20260625171151544.png)

### 4. 查看提交日志

当讲代码提交到了本地仓库以后，我们可以查看提交的历史记录，可以使用一下命令：

```bash
git log
```

效果如图所示：

![image-20260625182905231](static/docs/Git使用教程/images/image-20260625182905231.png)

当有大量提交记录时，使用`git log`指令查看记录会不方便，此时我们可以使用如下指令，更直观明了：

```bash
git-log
```

效果如图所示：

![image-20260625183339999](static/docs/Git使用教程/images/image-20260625183339999.png)

说明：该指令为简化后指令，简化前为`git log --pretty=oneline --abbrev-commit --all --graph --decorate`。

### 5. 版本回退

使用git管理代码的一个重要原因便是git可以进行版本回退，浏览编辑之前的提交，版本回溯分别为三种方式。

1. soft

   取消提交，暂存区和工作区都不回溯，即仅取消commit操作，不取消add操作，适用于合并多次commit，修改提交备注；

   ```bash
   git reset --soft commitID
   ```

2. mixed

   取消提交，暂存区文件回溯，工作区文件不回溯，即取消commit、add操作，适用于取消`git add`操作；

   ```bash
   git reset --mixed commitID
   ```

3. hard

   取消提交，暂存区和工作区都回溯，适用于彻底回到某个版本。

   ```bash
   git reset --hard commitID
   ```

说明：commitID（提交哈希值）为每次提交生成的唯一40位十六进制字符串，相当于每个版本的身份证，使用时取前七位即可。

![image-20260625192828282](static/docs/Git使用教程/images/image-20260625192828282.png)

### 6. 添加文件至忽略列表

一般我们总会有些文件由于各种原因无需纳入Git管理，也不希望它们总出现在未跟踪文件列表中。这列文件通常都是一些自动生成的文件，比如日志文件，或者编译过程中创建的临时文件，以及视频之类的大文件等。在这种情况下，我们可以在工作目录中创建一个名为`.gitignore`的文件（文件名固定），列出要忽略的文件（可使用通配符）。下面是一个示例：

```bash
*.a
!lib.a
/TODO
build/
doc/*.txt
doc/**/*.pdf
```

---

## 三、分支操作

